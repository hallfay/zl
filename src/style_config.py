from typing import Dict, Set

class StyleConfig:
    # Markdown 标题样式
    HEADERS = {
        'main': '# {}',
        'section': '## {}',
        'subsection': '### {}'
    }
    
    # 代码文件类型配置
    CODE_FILE_TYPES: Set[str] = {
        # 常见编程语言
        '.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts',
        # Web开发
        '.html', '.css', '.jsx', '.tsx', '.vue', '.php',
        # 数据文件
        '.sql', '.json', '.yaml', '.yml',
        # 配置文件
        '.xml', '.ini', '.conf', '.toml',
        # 脚本文件
        '.sh', '.bash', '.ps1', '.bat'
    }
    
    # 文档文件类型
    DOC_FILE_TYPES: Set[str] = {
        '.md', '.txt', '.rst', '.doc', '.docx', '.pdf'
    }
    
    # 语法高亮映射
    SYNTAX_HIGHLIGHT_MAP: Dict[str, str] = {
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.go': 'go',
        '.rs': 'rust',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.jsx': 'jsx',
        '.tsx': 'tsx',
        '.vue': 'vue',
        '.php': 'php',
        '.sql': 'sql',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.xml': 'xml',
        '.sh': 'bash',
        '.bash': 'bash'
    }
    
    # Markdown 样式模板
    TEMPLATES = {
        'file_header': """# {filename}

{badges}

## 文件信息
- 路径: `{filepath}`
- 类型: {filetype}
- 大小: {filesize}
""",
        'code_section': """## 代码分析
{summary}

### 主要功能
{functions}

### 特性
{features}

### 源代码
```{language}
{code}
```""",
        'doc_section': """## 文档内容
{content}""",
        
        'directory_header': """# {dirname} 目录文档

## 目录信息
- 路径: `{dirpath}`
- 文件数量: {filecount}
- 子目录数量: {subdircount}
""",
        'toc': """## 目录
{toc_content}
""",
        'separator': "\n---\n"
    }
    
    @classmethod
    def is_code_file(cls, file_path: str) -> bool:
        """判断是否为代码文件"""
        return any(file_path.lower().endswith(ext) for ext in cls.CODE_FILE_TYPES)
    
    @classmethod
    def is_doc_file(cls, file_path: str) -> bool:
        """判断是否为文档文件"""
        return any(file_path.lower().endswith(ext) for ext in cls.DOC_FILE_TYPES)
    
    @classmethod
    def get_syntax_highlight(cls, file_path: str) -> str:
        """获取文件的语法高亮类型"""
        ext = ''.join(Path(file_path).suffixes)
        return cls.SYNTAX_HIGHLIGHT_MAP.get(ext, 'plaintext')
    
    @classmethod
    def format_file_size(cls, size_in_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} TB" 