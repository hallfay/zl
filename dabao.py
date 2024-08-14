import os

def process_directory(directory, output_file, base_path):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, base_path)
            
            # Skip .git directory and its contents
            if '.git' in relative_path.split(os.sep):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                output_file.write(f"## {relative_path}\n\n")
                output_file.write("```\n")
                output_file.write(content)
                output_file.write("\n```\n\n")
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

def main():
    repo_path = input("Enter the path to the downloaded repository: ")
    output_filename = input("Enter the name for the output markdown file: ")

    if not output_filename.endswith('.md'):
        output_filename += '.md'

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        process_directory(repo_path, output_file, repo_path)

    print(f"Repository contents have been saved to {output_filename}")

if __name__ == "__main__":
    main()