import os
from pathlib import Path
from typing import List, Dict, Set
from .analyzer import CodeAnalyzer
from .style_config import StyleConfig

class DocGenerator:
    def __init__(self):
        self.content_hash: Set[str] = set()
        self.generated_docs: Dict[str, str] = {}
        self.analyzer = CodeAnalyzer()
        self.style = StyleConfig()

    def generate_file_doc(self, file_path: str, content: str, is_code: bool) -> str:
        """为单个文件生成markdown文档"""
        file_info = self._get_file_info(file_path)
        
        # 生成文件头部
        doc_content = self.style.TEMPLATES['file_header'].format(
            filename=file_info['name'],
            badges=self._generate_badges(file_info),
            filepath=file_info['path'],
            filetype=file_info['type'],
            filesize=file_info['size']
        )

        if is_code:
            # 使用AI分析代码
            analysis = self.analyzer.analyze_code(file_path, content)
            
            # 生成代码部分
            doc_content += self.style.TEMPLATES['code_section'].format(
                summary=analysis['summary'],
                functions=self._format_list(analysis['functions']),
                features=self._format_list(analysis['features']),
                language=self.style.get_syntax_highlight(file_path),
                code=content
            )
        else:
            # 生成文档部分
            doc_content += self.style.TEMPLATES['doc_section'].format(
                content=content
            )

        return doc_content

    def generate_directory_doc(self, directory: str, files: List[str]) -> str:
        """为目录生成markdown文档"""
        dir_info = self._get_directory_info(directory, files)
        
        # 生成目录头部
        doc_content = self.style.TEMPLATES['directory_header'].format(
            dirname=dir_info['name'],
            dirpath=dir_info['path'],
            filecount=dir_info['file_count'],
            subdircount=dir_info['subdir_count']
        )
        
        # 使用AI分析目录结构
        analysis = self.analyzer.analyze_directory(directory, files)
        
        # 添加目录概述
        doc_content += f"\n## 目录概述\n{analysis['summary']}\n\n"
        
        # 添加目录结构
        doc_content += "## 目录结构\n"
        doc_content += self._generate_tree_structure(directory, files)
        
        # 添加结构分析
        if analysis['structure']:
            doc_content += "\n## 结构分析\n"
            doc_content += self._format_list(analysis['structure'])
        
        return doc_content

    def save_doc(self, output_path: str, content: str):
        """保存markdown文档"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.generated_docs[output_path] = content

    def merge_docs(self, output_path: str):
        """合并所有生成的文档"""
        # 生成目录
        toc_content = self._generate_toc()
        
        # 合并文档
        merged_content = "# 项目文档\n\n"
        merged_content += self.style.TEMPLATES['toc'].format(toc_content=toc_content)
        merged_content += "\n## 详细文档\n\n"
        
        # 合并文档内容
        for doc_path, content in self.generated_docs.items():
            if not self._is_content_duplicate(content):
                merged_content += f"{content}{self.style.TEMPLATES['separator']}"
        
        # 保存合并后的文档
        self.save_doc(output_path, merged_content)

    def _get_file_info(self, file_path: str) -> dict:
        """获取文件信息"""
        path = Path(file_path)
        return {
            'name': path.name,
            'path': str(path),
            'type': path.suffix,
            'size': self.style.format_file_size(path.stat().st_size)
        }

    def _get_directory_info(self, directory: str, files: List[str]) -> dict:
        """获取目录信息"""
        path = Path(directory)
        subdirs = set(str(Path(f).parent) for f in files) - {directory}
        return {
            'name': path.name,
            'path': str(path),
            'file_count': len(files),
            'subdir_count': len(subdirs)
        }

    def _generate_badges(self, file_info: dict) -> str:
        """生成文件徽章"""
        badges = []
        if self.style.is_code_file(file_info['path']):
            badges.append(f"![代码文件](https://img.shields.io/badge/类型-代码-blue)")
        elif self.style.is_doc_file(file_info['path']):
            badges.append(f"![文档文件](https://img.shields.io/badge/类型-文档-green)")
        return " ".join(badges)

    def _generate_tree_structure(self, directory: str, files: List[str]) -> str:
        """生成树形目录结构"""
        tree = []
        for file in sorted(files):
            rel_path = os.path.relpath(file, directory)
            indent = "  " * (rel_path.count(os.sep))
            tree.append(f"{indent}- {os.path.basename(file)}")
        return "\n".join(tree) + "\n"

    def _generate_toc(self) -> str:
        """生成文档目录"""
        toc = []
        for doc_path in self.generated_docs:
            name = Path(doc_path).stem
            toc.append(f"- [{name}](#{name.lower()})")
        return "\n".join(toc)

    def _format_list(self, items: List[str]) -> str:
        """格式化列表内容"""
        return "\n".join(f"- {item}" for item in items) + "\n"

    def _is_content_duplicate(self, content: str) -> bool:
        """检查内容是否重复"""
        content_hash = hash(content)
        if content_hash in self.content_hash:
            return True
        self.content_hash.add(content_hash)
        return False 