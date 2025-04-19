import os
import shutil
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType

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
    
    node = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "More text")
    ])
    print(node.to_html())

main()