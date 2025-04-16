
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

from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Expected a TextNode")
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
