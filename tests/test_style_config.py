import unittest
from src.style_config import StyleConfig

class TestStyleConfig(unittest.TestCase):
    def setUp(self):
        self.style = StyleConfig()

    def test_is_code_file(self):
        """测试代码文件识别"""
        # 测试各种代码文件
        self.assertTrue(self.style.is_code_file('test.py'))
        self.assertTrue(self.style.is_code_file('test.js'))
        self.assertTrue(self.style.is_code_file('test.java'))
        self.assertTrue(self.style.is_code_file('test.cpp'))
        
        # 测试非代码文件
        self.assertFalse(self.style.is_code_file('test.txt'))
        self.assertFalse(self.style.is_code_file('test.md'))
        self.assertFalse(self.style.is_code_file('test'))

    def test_is_doc_file(self):
        """测试文档文件识别"""
        # 测试各种文档文件
        self.assertTrue(self.style.is_doc_file('test.md'))
        self.assertTrue(self.style.is_doc_file('test.txt'))
        self.assertTrue(self.style.is_doc_file('test.rst'))
        
        # 测试非文档文件
        self.assertFalse(self.style.is_doc_file('test.py'))
        self.assertFalse(self.style.is_doc_file('test.js'))
        self.assertFalse(self.style.is_doc_file('test'))

    def test_get_syntax_highlight(self):
        """测试语法高亮类型获取"""
        self.assertEqual(self.style.get_syntax_highlight('test.py'), 'python')
        self.assertEqual(self.style.get_syntax_highlight('test.js'), 'javascript')
        self.assertEqual(self.style.get_syntax_highlight('test.unknown'), 'plaintext')

    def test_format_file_size(self):
        """测试文件大小格式化"""
        # 测试各种大小
        self.assertEqual(self.style.format_file_size(100), '100.00 B')
        self.assertEqual(self.style.format_file_size(1024), '1.00 KB')
        self.assertEqual(self.style.format_file_size(1024 * 1024), '1.00 MB')
        self.assertEqual(self.style.format_file_size(1024 * 1024 * 1024), '1.00 GB')

    def test_templates(self):
        """测试模板格式化"""
        # 测试文件头部模板
        header = self.style.TEMPLATES['file_header'].format(
            filename='test.py',
            badges='![测试](test)',
            filepath='/path/to/test.py',
            filetype='.py',
            filesize='1.00 KB'
        )
        self.assertIn('test.py', header)
        self.assertIn('/path/to/test.py', header)
        self.assertIn('.py', header)
        self.assertIn('1.00 KB', header)

        # 测试代码段模板
        code_section = self.style.TEMPLATES['code_section'].format(
            summary='测试摘要',
            functions='- 函数1\n- 函数2',
            features='- 特性1\n- 特性2',
            language='python',
            code='print("test")'
        )
        self.assertIn('测试摘要', code_section)
        self.assertIn('函数1', code_section)
        self.assertIn('特性1', code_section)
        self.assertIn('```python', code_section)

if __name__ == '__main__':
    unittest.main() 