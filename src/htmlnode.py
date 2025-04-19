class HTMLNode():

    def __init__(self, value=None, children=None, props=None, tag=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_str = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        return f" {props_str}"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(value, None, props, tag)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("ParentNode 'tag' must be a non-empty string")
        if not isinstance(children, list) or not all(isinstance(child, HTMLNode) for child in children):
            raise ValueError("ParentNode 'children' must be a list of HTMLNode instances")
        super().__init__(None, children, props, tag)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if not self.children:
            raise ValueError("ParentNode must have children")
        if not isinstance(self.children, list) or not all(isinstance(child, HTMLNode) for child in self.children):
            raise ValueError("ParentNode children must be a list of HTMLNode instances")
        props_str = self.props_to_html()
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

import re
from md_to_textnode import block_to_block_type, markdown_to_blocks, text_to_textnodes
from textnode import BlockType, TextNode, TextType

def text_node_to_html_node(text_node):
    """Convert a TextNode to an HTMLNode."""
    if not isinstance(text_node, TextNode):
        raise ValueError("Expected a TextNode")
        
    # Handle empty text based on type
    if not text_node.text:
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, "")
            case TextType.BOLD:
                return LeafNode("b", "")
            case TextType.ITALIC:
                return LeafNode("i", "")
            case TextType.CODE:
                return LeafNode("code", "")
            case TextType.LINK:
                return LeafNode("a", "", {"href": text_node.url or ""})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url or "", "alt": ""})
            case _:
                return LeafNode(None, "")
                
    # Handle non-empty text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextType: {text_node.text_type}")
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block.strip():  # Only process non-empty blocks
            if block.startswith("```"):
                # Handle code blocks
                html_node = code_to_html_node(block)
            else:
                html_node = block_to_html_node(block)
            children.append(html_node)
    
    # Ensure we have at least one child, even if it's just an empty paragraph
    if not children:
        children = [ParentNode("p", [LeafNode(None, "")])]
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
    

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def paragraph_to_html_node(block):
    lines = block.split("\n")
    # Join lines and normalize whitespace
    paragraph = " ".join([line.strip() for line in lines])
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    # Split the block into lines
    lines = block.split("\n")
    
    # Remove empty lines at the beginning and end
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    
    # Find the starting and ending lines with ```
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(lines):
        if line.strip() == "```":
            if start_index == -1:
                start_index = i
            else:
                end_index = i
                break
    
    if start_index != -1 and end_index != -1:
        # Get lines between the backticks and strip any common indentation
        content_lines = lines[start_index+1:end_index]
        
        # Remove common leading whitespace
        if content_lines:
            min_indent = min(len(line) - len(line.lstrip()) for line in content_lines if line.strip())
            content_lines = [line[min_indent:] if len(line) >= min_indent else line for line in content_lines]
        
        # Add trailing newline to match expected output
        content = "\n".join(content_lines) + "\n"
    else:
        # Fallback if backticks aren't found
        content = block
    
    # Create TextNode for the code content
    text_node = TextNode(content, TextType.TEXT)  # Use TextType.TEXT instead of TextType.CODE
    # Convert to HTML node
    code_html_node = text_node_to_html_node(text_node)
    # Wrap it in <pre><code> tags
    return ParentNode("pre", [ParentNode("code", [code_html_node])])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)