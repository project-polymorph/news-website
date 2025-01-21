import os
import re
import yaml
import shutil
from urllib.parse import urlparse

def load_config():
    with open('.github/url_dir_map_config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def extract_original_url(content):
    match = re.search(r'<!--\s*tcd_original_link\s+(.*?)\s*-->', content)
    return match.group(1) if match else None

def get_target_dir(url, config):
    if not url:
        return "未分类"
    
    domain = urlparse(url).netloc
    for mapping in config['url_mappings']:
        if mapping['domain'] in domain:
            return mapping['dir']
    return "未分类"

def get_unique_filename(target_path, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(target_path, filename)
    
    while os.path.exists(new_path):
        new_filename = f"{base}_{counter}{ext}"
        new_path = os.path.join(target_path, new_filename)
        counter += 1
    
    return new_path

def main():
    config = load_config()
    workspace_dir = 'workspace'

    # Create target directories if they don't exist
    for mapping in config['url_mappings']:
        dir_path = os.path.join(workspace_dir, mapping['dir'])
        os.makedirs(dir_path, exist_ok=True)

    # Process markdown files
    for root, _, files in os.walk(workspace_dir):
        for file in files:
            if not file.endswith('.md'):
                continue

            file_path = os.path.join(root, file)
            
            # Skip files that are already in target directories
            if any(mapping['dir'] in file_path for mapping in config['url_mappings']):
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            url = extract_original_url(content)
            target_dir = get_target_dir(url, config)
            target_dir_path = target_dir
            
            # Create target directory if it doesn't exist
            os.makedirs(target_dir_path, exist_ok=True)
            
            # Get unique filename in target directory
            new_file_path = get_unique_filename(target_dir_path, file)
            
            # Move file
            shutil.move(file_path, new_file_path)
            print(f"Moved {file} to {target_dir}")

if __name__ == "__main__":
    main()
