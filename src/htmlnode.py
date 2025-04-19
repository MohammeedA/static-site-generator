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

def text_to_children(text: str) -> list[HTMLNode]:
    """Convert text content to a list of HTMLNodes by parsing inline markdown"""
    nodes = text_to_textnodes(text)
    children = []
    
    for node in nodes:
        if isinstance(node, TextNode):
            html_node = text_node_to_html_node(node)
            children.append(html_node)
        else:
            raise ValueError("Expected a TextNode")
    
    return children
    

def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts markdown text to a single HTMLNode representing the complete document
    """
    blocks = markdown_to_blocks(markdown)
    if not blocks:
        return ParentNode("div", [LeafNode(None, "")])

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_children = text_to_children(block)
                block_node = ParentNode("p", block_children) if block_children else ParentNode("p", [LeafNode(None, "")])
                children.append(block_node)
            case BlockType.HEADING:
                # Extract heading level and content
                heading_parts = block.split(" ", 1)
                level = len(heading_parts[0])  # Count the # characters
                content = heading_parts[1] if len(heading_parts) > 1 else ""
                # Parse content for inline formatting
                block_children = text_to_children(content)
                block_node = ParentNode(f"h{level}", block_children) if block_children else ParentNode(f"h{level}", [LeafNode(None, "")])
                children.append(block_node)
            case BlockType.CODE:
                # Strip the triple backticks and get the content
                code_content = "\n".join(block.split("\n")[1:-1])  # Remove first and last lines (the backticks)
                # Create text node without parsing markdown
                # Create the nested structure
                pre_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])
                children.append(pre_node)
            case BlockType.QUOTE:
                block_children = process_quote(block)
                block_node = ParentNode("blockquote", block_children) if block_children else ParentNode("blockquote", [LeafNode(None, "")])
                children.append(block_node)
            case BlockType.UNORDERED_LIST:
                list_items = process_list(block)
                # Create the ul node
                block_node = ParentNode("ul", list_items) if list_items else ParentNode("ul", [LeafNode(None, "")])
                children.append(block_node)
            case BlockType.ORDERED_LIST:
                list_items = process_list(block)
                # Create the ol node
                block_node = ParentNode("ol", list_items) if list_items else ParentNode("ol", [LeafNode(None, "")])
                children.append(block_node)
            case _:
                raise ValueError(f"Invalid BlockType: {block_type}")
    return ParentNode("div", children) if children else ParentNode("div", [LeafNode(None, "")])

def process_list(block: str) -> list[HTMLNode]:
    """
    Process a block of text that represents a list and return a list of HTMLNode.
    """
    # Split the block into lines
    lines = block.strip().split("\n")
    
    # Create a list to hold the HTML nodes
    list_items = []
    
    for line in lines:
        # Remove the leading marker (-) and create li element
        content = line.strip()
        if content.startswith(("- ")):
            content = content[2:]  # Remove marker for unordered lists
        elif re.match(r"\d+\.\s", content):
            content = re.sub(r"\d+\.\s", "", content, 1)  # Remove marker for ordered lists
        
        item_children = text_to_children(content)
        list_items.append(ParentNode("li", item_children) if item_children else ParentNode("li", [LeafNode(None, "")]))
    
    return list_items

def process_quote(block):
    # Remove '>' markers and reassemble content
    lines = block.split('\n')
    cleaned_lines = []
    for line in lines:
        if line.startswith('> '):
            cleaned_lines.append(line[2:])  # Remove '> '
        elif line.startswith('>'):
            cleaned_lines.append(line[1:])  # Remove '>'
        else:
            cleaned_lines.append(line)  # Keep as is if no marker
    
    cleaned_content = '\n'.join(cleaned_lines)
    return text_to_children(cleaned_content)