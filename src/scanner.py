import os
from pathlib import Path
from typing import List, Set

class FileScanner:
    def __init__(self):
        self.ignore_dirs = {'.git', 'node_modules', '__pycache__', 'venv'}
        self.ignore_files = {'.DS_Store'}
        self.processed_files: Set[str] = set()

    def should_ignore(self, path: str) -> bool:
        """检查是否应该忽略该路径"""
        path_parts = Path(path).parts
        return any(ignore in path_parts for ignore in self.ignore_dirs) or \
               any(path.endswith(ignore) for ignore in self.ignore_files)

    def scan_directory(self, directory: str) -> List[str]:
        """扫描目录，返回所有需要处理的文件路径"""
        files_to_process = []
        
        for root, dirs, files in os.walk(directory):
            # 过滤掉需要忽略的目录
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                if not self.should_ignore(file_path) and file_path not in self.processed_files:
                    files_to_process.append(file_path)
                    self.processed_files.add(file_path)
        
        return files_to_process

    def is_code_file(self, file_path: str) -> bool:
        """判断是否为代码文件"""
        code_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts'}
        return Path(file_path).suffix in code_extensions 