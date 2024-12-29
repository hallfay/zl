import unittest
import os
import tempfile
from src.reader import FileReader

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.reader = FileReader()
        # 创建临时测试目录和文件
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        self.test_content = 'Hello, World!'
        
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(self.test_content)

    def tearDown(self):
        # 清理测试目录
        import shutil
        shutil.rmtree(self.test_dir)

    def test_read_file(self):
        """测试文件读取功能"""
        # 测试正常读取
        content = self.reader.read_file(self.test_file)
        self.assertEqual(content, self.test_content)
        
        # 测试缓存功能
        self.assertIn(self.test_file, self.reader.content_cache)
        
        # 测试读取不存在的文件
        content = self.reader.read_file('nonexistent.txt')
        self.assertIsNone(content)

    def test_get_file_info(self):
        """测试获取文件信息功能"""
        info = self.reader.get_file_info(self.test_file)
        
        self.assertEqual(info['name'], 'test.txt')
        self.assertEqual(info['extension'], '.txt')
        self.assertEqual(info['size'], len(self.test_content))
        self.assertEqual(info['path'], self.test_file)
        self.assertEqual(info['parent_dir'], self.test_dir)

    def test_clear_cache(self):
        """测试清除缓存功能"""
        # 先读取文件以填充缓存
        self.reader.read_file(self.test_file)
        self.assertIn(self.test_file, self.reader.content_cache)
        
        # 清除缓存
        self.reader.clear_cache()
        self.assertEqual(len(self.reader.content_cache), 0)

if __name__ == '__main__':
    unittest.main() 