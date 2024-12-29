import os
from src.scanner import FileScanner
from src.reader import FileReader
from src.generator import DocGenerator
from dotenv import load_dotenv

def is_text_file(filename):
    # 定义支持的文本文件扩展名
    text_extensions = {'.txt', '.md', '.json', '.py', '.js', '.html', '.css', '.xml', '.yml', '.yaml', '.conf'}
    # 定义要排除的二进制文件扩展名
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.doc', '.docx', '.xls', '.xlsx'}
    
    ext = os.path.splitext(filename)[1].lower()
    return ext in text_extensions and ext not in binary_extensions

def read_file_content(file_path):
    if not is_text_file(file_path):
        print(f"跳过非文本文件: {file_path}")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"编码错误，跳过文件: {file_path}")
        return None
    except Exception as e:
        print(f"读取文件错误 {file_path}: {str(e)}")
        return None

def get_env_list(env_var: str, default: list) -> list:
    """从环境变量获取列表配置"""
    value = os.getenv(env_var)
    if value:
        return [item.strip() for item in value.split(',')]
    return default

def main(target_directory: str = None, output_directory: str = None):
    """
    主程序入口
    :param target_directory: 要扫描的目标目录（可选，优先使用环境变量）
    :param output_directory: 文档输出目录（可选，优先使用环境变量）
    """
    # 加载环境变量
    load_dotenv()
    
    # 获取目录配置
    target_directory = target_directory or os.getenv('INPUT_DIR')
    output_directory = output_directory or os.getenv('OUTPUT_DIR', 'docs')
    
    if not target_directory:
        print("错误: 未指定目标目录。请在.env文件中设置INPUT_DIR或通过命令行参数指定。")
        return
    
    # 获取忽略配置
    ignore_dirs = get_env_list('IGNORE_DIRS', ['.git', 'node_modules', '__pycache__', 'venv'])
    ignore_files = get_env_list('IGNORE_FILES', ['.DS_Store'])
    
    print(f"开始分析目录: {target_directory}")
    print(f"文档输出目录: {output_directory}")
    print(f"忽略的目录: {ignore_dirs}")
    print(f"忽略的文件: {ignore_files}")
    
    # 初始化各个模块
    scanner = FileScanner()
    scanner.ignore_dirs = set(ignore_dirs)  # 更新忽略目录配置
    scanner.ignore_files = set(ignore_files)  # 更新忽略文件配置
    
    reader = FileReader()
    generator = DocGenerator()

    # 扫描目录获取文件列表
    files = scanner.scan_directory(target_directory)
    print(f"找到 {len(files)} 个文件需要处理")
    
    # 处理每个文件
    processed_count = 0
    for file_path in files:
        # 跳过非文本文件
        if not is_text_file(file_path):
            continue
            
        # 读取文件内容
        content = reader.read_file(file_path)
        if content is None:
            continue

        # 判断是否为代码文件
        is_code = scanner.is_code_file(file_path)
        
        # 生成文档
        doc_content = generator.generate_file_doc(file_path, content, is_code)
        
        # 确定输出路径
        rel_path = os.path.relpath(file_path, target_directory)
        output_path = os.path.join(output_directory, f"{rel_path}.md")
        
        # 保存文档
        generator.save_doc(output_path, doc_content)
        processed_count += 1
        print(f"处理进度: {processed_count}/{len(files)} - {rel_path}")

    print("生成目录文档...")
    # 为目录生成文档
    dir_doc = generator.generate_directory_doc(target_directory, files)
    generator.save_doc(os.path.join(output_directory, "directory_structure.md"), dir_doc)

    print("合并文档...")
    # 合并所有文档
    generator.merge_docs(os.path.join(output_directory, "complete_documentation.md"))
    
    print(f"文档生成完成！共处理 {processed_count} 个文件")
    print(f"文档已保存到: {output_directory}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        main(target_dir, output_dir)
    else:
        main() 