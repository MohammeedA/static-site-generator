import os
import shutil
from htmlnode import LeafNode, ParentNode, markdown_to_html_node
from textnode import TextNode, TextType
from md_to_textnode import extract_title

def generate_page(from_path, template_path, dest_path):
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

def main():
    # Copy static directory to public
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
    copy_directory(static_dir, public_dir)
    
    # Generate the index page from markdown to HTML
    content_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template.html")
    
    # Convert index.md to index.html
    index_md_path = os.path.join(content_dir, "index.md")
    index_html_path = os.path.join(public_dir, "index.html")
    generate_page(index_md_path, template_path, index_html_path)

main()