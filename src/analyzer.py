import os
from typing import Optional, List, Dict
from openai import OpenAI
from dotenv import load_dotenv

class CodeAnalyzer:
    # 不同文件类型的分析提示
    ANALYSIS_PROMPTS: Dict[str, str] = {
        '.json': """你是一个专业的配置文件分析专家。请详细分析这个JSON文件的内容，包括：
1. 这个配置文件的主要用途是什么？
2. 包含了哪些关键配置项？
3. 这些配置会产生什么效果？
4. 有什么需要特别注意的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。""",

        '.yml': """你是一个专业的YAML配置文件分析专家。请详细分析这个YAML文件的内容，包括：
1. 这个配置文件的主要用途是什么？
2. 包含了哪些关键配置项和层级结构？
3. 这些配置会如何影响系统行为？
4. 配置之间存在什么依赖关系？
5. 有什么需要特别注意的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。""",

        '.ts': """你是一个TypeScript代码分析专家。请详细分析这段TypeScript代码，包括：
1. 代码的主要功能和目的是什么？
2. 包含了哪些关键的类型定义和接口？
3. 实现了什么具体的业务逻辑？
4. 使用了哪些TypeScript特有的功能？
5. 类型安全性如何？
6. 代码的组织结构和设计模式是什么？
7. 有什么可以改进的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。""",

        '.js': """你是一个JavaScript代码分析专家。请详细分析这段JavaScript代码，包括：
1. 代码的主要功能和目的是什么？
2. 包含了哪些关键函数和方法？
3. 使用了哪些JavaScript特性？
4. 实现了什么具体的业务逻辑？
5. 代码的组织方式和模块化程度如何？
6. 有什么需要注意的性能或兼容性问题？
7. 有什么可以改进的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。""",

        '.py': """你是一个Python代码分析专家。请详细分析这段Python代码，包括：
1. 代码的主要功能和目的是什么？
2. 包含了哪些关键类和函数？
3. 使用了哪些Python特有的语言特性？
4. 实现了什么具体的业务逻辑？
5. 代码的可读性和Pythonic程度如何？
6. 异常处理是否完善？
7. 有什么可以改进的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。""",

        'default': """你是一个代码分析专家。请详细分析这段代码，包括：
1. 代码的主要功能和目的是什么？
2. 包含了哪些关键函数/方法？
3. 实现了什么具体的业务逻辑？
4. 代码的特点和亮点是什么？
5. 代码质量和可维护性如何？
6. 有什么需要注意或可以改进的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。"""
    }

    def __init__(self):
        load_dotenv()  # 加载环境变量
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('OPENAI_API_BASE')
        self.model = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
        else:
            self.client = None

    def analyze_code(self, file_path: str, content: str) -> dict:
        """分析代码文件的功能和结构"""
        if not self.client:
            return self._get_default_analysis(file_path)

        try:
            # 根据文件类型获取对应的分析提示
            file_ext = os.path.splitext(file_path)[1].lower()
            system_prompt = self.ANALYSIS_PROMPTS.get(file_ext, self.ANALYSIS_PROMPTS['default'])

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"请分析这个文件的内容：\n\n{content}"}
                ]
            )
            
            analysis = response.choices[0].message.content
            
            # 进行第二轮分析，获取更多细节
            detail_prompt = self._get_detail_prompt(file_ext)
            
            detail_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个代码分析专家。"},
                    {"role": "assistant", "content": analysis},
                    {"role": "user", "content": detail_prompt}
                ]
            )
            
            detail_analysis = detail_response.choices[0].message.content
            
            return {
                'summary': f"## 基础分析\n{analysis}\n\n## 深入分析\n{detail_analysis}",
                'functions': self._extract_functions(analysis),
                'features': self._extract_features(detail_analysis)
            }
        except Exception as e:
            print(f"AI分析失败: {str(e)}")
            return self._get_default_analysis(file_path)

    def _get_detail_prompt(self, file_ext: str) -> str:
        """获取详细分析的提示"""
        if file_ext in ['.json', '.yml', '.yaml']:
            return """基于上述分析，请再深入探讨以下方面：
1. 这个配置文件在系统中扮演什么角色？
2. 修改配置时需要注意哪些依赖关系？
3. 如何确保配置的正确性和安全性？
4. 这些配置可能会影响系统的哪些部分？

请用清晰的条目列表方式输出分析结果。每个要点前使用'* '标记。"""
        elif file_ext in ['.ts', '.js', '.jsx', '.tsx']:
            return """基于上述分析，请再深入探讨以下方面：
1. 这段代码在前端架构中的作用是什么,实现了哪些功能？
2. 与其他组件或模块的交互方式如何？
3. 有哪些潜在的性能优化空间？
4. 代码的可测试性如何？
5. 如何确保代码的安全性和稳定性？

请用清晰的条目列表方式输出分析结果。每个要点前使用'* '标记。"""
        elif file_ext == '.py':
            return """基于上述分析，请再深入探讨以下方面：
1. 这段Python代码的设计模式和架构特点是什么？
2. 代码的可扩展性和重用性如何？
3. 是否遵循了Python的最佳实践？
4. 有哪些可能的性能瓶颈？
5. 如何改进代码的测试覆盖率？

请用清晰的条目列表方式输出分析结果。每个要点前使用'* '标记。"""
        else:
            return f"""基于上述分析，请再深入探讨以下方面：
1. 这个{file_ext}文件在整个系统中可能扮演什么角色？
2. 如果要修改或配置它，需要注意什么？
3. 它可能会和哪些其他文件或系统产生交互？
4. 代码质量和可维护性如何？
5. 有哪些潜在的改进空间？

请用清晰的条目列表方式输出分析结果。每个要点前使用'* '标记。"""

    def analyze_directory(self, directory: str, files: List[str]) -> dict:
        """分析目录的整体结构和功能"""
        if not self.client:
            return self._get_default_directory_analysis(directory)

        try:
            files_str = "\n".join(files)
            system_prompt = """你是一个代码结构分析专家。请详细分析这个目录结构，包括：
1. 这个目录的主要用途是什么？
2. 包含了哪些类型的文件？
3. 文件之间可能存在什么关联？
4. 这个目录结构反映了什么样的项目特点？
5. 有什么需要特别注意的地方？

请用清晰的条目列表方式输出分析结果。每个要点前使用'- '标记。"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"请分析这个目录的结构：\n\n{files_str}"}
                ]
            )
            
            analysis = response.choices[0].message.content
            
            # 进行第二轮分析，获取更多细节
            detail_prompt = """基于上述分析，请再深入探讨以下方面：
1. 这个目录结构如何支持项目的功能实现？
2. 文件组织方式有什么优点和可能的改进空间？
3. 对于项目的维护和扩展有什么建议？
4. 是否存在潜在的架构问题？
5. 如何提高代码的可维护性和可扩展性？

请用清晰的条目列表方式输出分析结果。每个要点前使用'* '标记。"""
            
            detail_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个代码结构分析专家。"},
                    {"role": "assistant", "content": analysis},
                    {"role": "user", "content": detail_prompt}
                ]
            )
            
            detail_analysis = detail_response.choices[0].message.content
            
            return {
                'summary': f"## 目录概述\n{analysis}\n\n## 深入分析\n{detail_analysis}",
                'structure': self._extract_structure(analysis + "\n" + detail_analysis)
            }
        except Exception as e:
            print(f"AI分析失败: {str(e)}")
            return self._get_default_directory_analysis(directory)

    def _get_default_analysis(self, file_path: str) -> dict:
        """生成默认的文件分析结果"""
        return {
            'summary': f'文件 {file_path} 的功能分析',
            'functions': ['需要进一步分析'],
            'features': ['需要进一步分析']
        }

    def _get_default_directory_analysis(self, directory: str) -> dict:
        """生成默认的目录分析结果"""
        return {
            'summary': f'目录 {directory} 的结构分析',
            'structure': ['需要进一步分析']
        }

    def _extract_functions(self, analysis: str) -> List[str]:
        """从分析结果中提取函数列表"""
        return [line.strip() for line in analysis.split('\n') if line.strip().startswith('- ')]

    def _extract_features(self, analysis: str) -> List[str]:
        """从分析结果中提取特性列表"""
        return [line.strip() for line in analysis.split('\n') if line.strip().startswith('* ')]

    def _extract_structure(self, analysis: str) -> List[str]:
        """从分析结果中提取结构信息"""
        return [line.strip() for line in analysis.split('\n') if line.strip()] 