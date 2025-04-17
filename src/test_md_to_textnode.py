import unittest
from md_to_textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        nodes = [node]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("*bold* and *more bold*", TextType.TEXT)
        nodes = [node]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text, "more bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)

    def test_no_delimiters(self):
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        nodes = [node]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text without delimiters")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_invalid_markdown(self):
        node = TextNode("This is *invalid markdown", TextType.TEXT)
        nodes = [node]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertTrue(f"Closing delimiter not found: *" in str(context.exception))

    def test_non_TEXT_node(self):
        node = TextNode("*already bold*", TextType.BOLD)
        nodes = [node]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "*already bold*")
        self.assertEqual(result[0].text_type, TextType.BOLD)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)
    
    def test_extract_markdown_links_multiple(self):
        text = "Here's [one link](https://example.com) and [another link](https://test.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("one link", "https://example.com"),
            ("another link", "https://test.com")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_with_no_links(self):
        text = "Plain text without any links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_image(self):
        text = "![image](https://example.com/img.jpg) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_with_special_chars(self):
        text = "[link with spaces](https://example.com/path%20with%20spaces)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link with spaces", "https://example.com/path%20with%20spaces")], matches)

if __name__ == '__main__':
    unittest.main()