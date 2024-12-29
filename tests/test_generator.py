import unittest
import os
import tempfile
from src.generator import DocGenerator

class TestDocGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DocGenerator()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_generate_file_doc(self):
        """测试生成文件文档功能"""
        # 测试代码文件文档生成
        code_content = 'def test():\n    print("Hello")'
        code_doc = self.generator.generate_file_doc('test.py', code_content, True)
        
        self.assertIn('# test.py', code_doc)
        self.assertIn('## 功能描述', code_doc)
        self.assertIn('```py', code_doc)
        self.assertIn(code_content, code_doc)
        
        # 测试普通文件文档生成
        text_content = 'Hello, World!'
        text_doc = self.generator.generate_file_doc('test.txt', text_content, False)
        
        self.assertIn('# test.txt', text_doc)
        self.assertIn('## 文件内容', text_doc)
        self.assertIn(text_content, text_doc)

    def test_generate_directory_doc(self):
        """测试生成目录文档功能"""
        test_files = [
            os.path.join(self.test_dir, 'test1.py'),
            os.path.join(self.test_dir, 'test2.js'),
            os.path.join(self.test_dir, 'subfolder/test3.txt')
        ]
        
        doc = self.generator.generate_directory_doc(self.test_dir, test_files)
        
        self.assertIn('# ' + os.path.basename(self.test_dir), doc)
        self.assertIn('## 目录结构', doc)
        for file in test_files:
            rel_path = os.path.relpath(file, self.test_dir)
            self.assertIn(rel_path, doc)

    def test_save_and_merge_docs(self):
        """测试保存和合并文档功能"""
        # 生成并保存一些测试文档
        docs = {
            'test1.md': '# Test 1\nContent 1',
            'test2.md': '# Test 2\nContent 2',
            'test3.md': '# Test 1\nContent 1'  # 重复内容
        }
        
        for name, content in docs.items():
            path = os.path.join(self.test_dir, name)
            self.generator.save_doc(path, content)
        
        # 测试合并文档
        merged_path = os.path.join(self.test_dir, 'merged.md')
        self.generator.merge_docs(merged_path)
        
        # 验证合并结果
        with open(merged_path, 'r') as f:
            merged_content = f.read()
            
        self.assertIn('# 项目文档', merged_content)
        self.assertIn('## 目录', merged_content)
        self.assertIn('Content 1', merged_content)
        self.assertIn('Content 2', merged_content)
        # 确保重复内容只出现一次
        self.assertEqual(merged_content.count('Content 1'), 1)

    def test_content_duplicate_detection(self):
        """测试内容重复检测功能"""
        content1 = "Test content 1"
        content2 = "Test content 2"
        
        # 第一次检查不应该报告重复
        self.assertFalse(self.generator._is_content_duplicate(content1))
        self.assertFalse(self.generator._is_content_duplicate(content2))
        
        # 重复内容应该被检测出来
        self.assertTrue(self.generator._is_content_duplicate(content1))
        self.assertTrue(self.generator._is_content_duplicate(content2))

if __name__ == '__main__':
    unittest.main() 