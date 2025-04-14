import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    
    """
    TEST EQUALS FOR DIFFERENT TEXT TYPES
    """
    def test_eq_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)
    
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
    
    def test_eq_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)
    
    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_eq_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node, node2)
    """
    ####################
    """
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is also a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_types(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.NORMAL, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.NORMAL, "www.vecka.nu")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()