import os
import sys
import shutil
from htmlnode import LeafNode, ParentNode, markdown_to_html_node
from textnode import TextNode, TextType
from md_to_textnode import extract_title

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Create any necessary directories for the destination path
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML and get the title
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace root paths with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)

def copy_directory(src, dst):
    # First, remove the destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    # Create the destination directory
    os.makedirs(dst)
    
    # Walk through the source directory
    for root, dirs, files in os.walk(src):
        # Calculate the corresponding destination path
        relative_path = os.path.relpath(root, src)
        dst_root = os.path.join(dst, relative_path)
        
        # Create all subdirectories
        for dir_name in dirs:
            dst_dir = os.path.join(dst_root, dir_name)
            print(f"Creating directory: {dst_dir}")
            os.makedirs(dst_dir, exist_ok=True)
        
        # Copy all files
        for file_name in files:
            src_file = os.path.join(root, file_name)
            dst_file = os.path.join(dst_root, file_name)
            print(f"Copying file: {src_file} -> {dst_file}")
            shutil.copy2(src_file, dst_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    # Walk through all files and directories in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        # Calculate the relative path from content directory
        rel_path = os.path.relpath(root, dir_path_content)
        
        # For each markdown file
        for file in files:
            if file.endswith('.md'):
                # Get the full source path of the markdown file
                src_file = os.path.join(root, file)
                
                # Calculate destination path:
                # 1. Get the relative directory structure
                # 2. Replace .md with .html
                dest_file_name = 'index.html' if file == 'index.md' else file.replace('.md', '.html')
                dest_file = os.path.join(dest_dir_path, rel_path, dest_file_name)
                
                # Generate the HTML page with basepath
                generate_page(src_file, template_path, dest_file, basepath)

def main():
    # Get basepath from command line argument or default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Copy static directory to docs
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    copy_directory(static_dir, docs_dir)
    
    # Generate all pages from markdown to HTML
    content_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template.html")
    
    # Generate all pages recursively with basepath
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)

if __name__ == "__main__":
    main()