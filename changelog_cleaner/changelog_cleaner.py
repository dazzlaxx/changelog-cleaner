import re
from collections import Counter

def remove_comment_blocks(input_file, output_file):
    encodings = ['utf-8', 'cp1251', 'cp1252', 'latin-1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as file:
                content = file.read()
            
            content = re.sub(r'/\*[\s\S]*?\*/', '', content)
            
            content = re.sub(r'===.*?(?=\n\s*\n|\Z)', '', content, flags=re.DOTALL)
            
            content = re.sub(r'//.*?\n', '\n', content)
            
            content = re.sub(r'!!!.*?\n', '\n', content)
            
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = content.strip()
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Successful: {encoding}")
            print(f"Output file: {output_file}")
            return True, content
            
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f'File not found: {input_file}')
            return False, None
        except Exception as e:
            print(f'Error: {e}')
            return False, None
    
    print(f"Failed to read file with any encoding: {input_file}")
    return False, None

def check_version_uniqueness(content):
    version_pattern = r'##\s+\d+\.\d+\s*-\s*\d{4}-\d{2}-\d{2}'
    versions = re.findall(version_pattern, content)
    
    print(f"Found versions: {versions}")  
    print(f"Number of versions found: {len(versions)}")
    print(f"Unique versions: {len(set(versions))}")
    
    if len(versions) != len(set(versions)):
        version_counts = Counter(versions)
        duplicates = [v for v, count in version_counts.items() if count > 1]
        return False, duplicates
    
    return True, []

if __name__ == '__main__':
    input_filename = 'CHANGELOG for developers.md'
    output_filename = 'CHANGELOG.md'
    
    success, cleaned_content = remove_comment_blocks(input_filename, output_filename)
    
    if success and cleaned_content:
        print("=== FIRST 500 CHARACTERS AFTER CLEANING ===")
        print(cleaned_content[:500] + "..." if len(cleaned_content) > 500 else cleaned_content)
        print("===========================================")
        
        is_unique, duplicates = check_version_uniqueness(cleaned_content)
        if not is_unique:
            print(f"Duplicate versions found: {', '.join(duplicates)}")
        else:
            print('All versions are unique')
    else:
        print('Failed to process the file')