from textnode import TextNode, TextType

def main():
    text = "This is some anchor text"
    text_type = TextType.LINK
    link = "https://www.boot.dev"
    text_node = TextNode(text, text_type, link)
    print(text_node)

main()