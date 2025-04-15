import unittest

from htmlnode import text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNodeToHtml(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_text_node(self):
        # Test with None
        with self.assertRaises(ValueError):
            text_node_to_html_node(None)
        
        # Test with invalid type
        with self.assertRaises(ValueError):
            text_node_to_html_node("not a TextNode")

    def test_empty_text_node(self):
        # Test with empty string
        node = TextNode("", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

        # Test bold
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "")

        # Test italic
        node = TextNode("", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "")

        # Test code
        node = TextNode("", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "")

if __name__ == '__main__':
    unittest.main()