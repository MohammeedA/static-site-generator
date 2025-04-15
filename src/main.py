from leafnode import LeafNode
from textnode import TextNode, TextType

def main():
    text = "This is some anchor text"
    text_type = TextType.LINK
    link = "https://www.boot.dev"
    text_node = TextNode(text, text_type, link)
    print(text_node)
    node = LeafNode("Click me", "a", {"href": "https://www.example.com"})
    print(node.to_html(), '<a href="https://www.example.com">Click me</a>')

main()