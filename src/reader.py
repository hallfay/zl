import os
from pathlib import Path
from typing import Optional, Dict

class FileReader:
    def __init__(self):
        self.content_cache: Dict[str, str] = {}

    def read_file(self, file_path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            if file_path in self.content_cache:
                return self.content_cache[file_path]

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.content_cache[file_path] = content
                return content
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return None

    def get_file_info(self, file_path: str) -> dict:
        """获取文件信息"""
        path = Path(file_path)
        return {
            'name': path.name,
            'extension': path.suffix,
            'size': os.path.getsize(file_path),
            'path': str(path),
            'parent_dir': str(path.parent)
        }

    def clear_cache(self):
        """清除缓存"""
        self.content_cache.clear() 