import unittest
import os
import tempfile
from pathlib import Path
from src.scanner import FileScanner

class TestFileScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = FileScanner()
        # 创建临时测试目录
        self.test_dir = tempfile.mkdtemp()
        
        # 创建测试文件结构
        self.create_test_files()

    def create_test_files(self):
        # 创建一些测试文件
        files = [
            'test.py',
            'test.js',
            'test.txt',
            '.DS_Store',
            'node_modules/test.js',
            '__pycache__/cache.pyc'
        ]
        
        for file_path in files:
            full_path = os.path.join(self.test_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write('test content')

    def tearDown(self):
        # 清理测试目录
        import shutil
        shutil.rmtree(self.test_dir)

    def test_should_ignore(self):
        """测试文件忽略功能"""
        # 应该被忽略的文件
        self.assertTrue(self.scanner.should_ignore(os.path.join(self.test_dir, 'node_modules/test.js')))
        self.assertTrue(self.scanner.should_ignore(os.path.join(self.test_dir, '.DS_Store')))
        
        # 不应该被忽略的文件
        self.assertFalse(self.scanner.should_ignore(os.path.join(self.test_dir, 'test.py')))
        self.assertFalse(self.scanner.should_ignore(os.path.join(self.test_dir, 'test.txt')))

    def test_scan_directory(self):
        """测试目录扫描功能"""
        files = self.scanner.scan_directory(self.test_dir)
        
        # 验证扫描结果
        self.assertEqual(len(files), 3)  # 应该只有3个文件（test.py, test.js, test.txt）
        self.assertTrue(any(f.endswith('test.py') for f in files))
        self.assertTrue(any(f.endswith('test.js') for f in files))
        self.assertTrue(any(f.endswith('test.txt') for f in files))

    def test_is_code_file(self):
        """测试代码文件识别功能"""
        self.assertTrue(self.scanner.is_code_file('test.py'))
        self.assertTrue(self.scanner.is_code_file('test.js'))
        self.assertTrue(self.scanner.is_code_file('test.java'))
        self.assertFalse(self.scanner.is_code_file('test.txt'))
        self.assertFalse(self.scanner.is_code_file('test.md'))

if __name__ == '__main__':
    unittest.main() 