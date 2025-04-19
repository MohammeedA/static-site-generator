import unittest
from md_to_textnode import split_nodes_delimiter, text_to_textnodes
from md_to_textnode import extract_markdown_images
from md_to_textnode import extract_markdown_links
from md_to_textnode import split_nodes_image
from md_to_textnode import markdown_to_blocks
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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode("Text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_images_non_text_node(self):
        node = TextNode("![img](url)", TextType.BOLD)  
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Start ![first](url1) middle", TextType.TEXT),
            TextNode("Not an image", TextType.BOLD),
            TextNode("End ![second](url2)", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" middle", TextType.TEXT),
            TextNode("Not an image", TextType.BOLD),
            TextNode("End ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2")
        ]
        self.assertListEqual(expected, result)
    
    def test_split_images_with_special_chars(self):
        node = TextNode(
            "![image with spaces](https://example.com/img%20name.jpg)",
            TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("image with spaces", TextType.IMAGE, "https://example.com/img%20name.jpg")
        ]
        self.assertListEqual(expected, result)
    
    def test_split_images_consecutive(self):
        node = TextNode(
            "![first](url1)![second](url2)",
            TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode("second", TextType.IMAGE, "url2")
        ]
        self.assertListEqual(expected, result)
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)
    
    # NESTED DELIMETERS NOT COVERED BY CODE YET
    # def test_text_to_textnodes_nested_bold_and_italic(self):
    #     text = "This is **bold and _italic_** text."
    #     result = text_to_textnodes(text)
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("bold and ", TextType.BOLD),
    #         TextNode("italic", TextType.ITALIC),
    #         TextNode(" text.", TextType.TEXT),
    #     ]
    #     self.assertListEqual(expected, result)

    def test_text_to_textnodes_multiple_images(self):
        text = "Here is ![image1](https://example.com/img1.png) and ![image2](https://example.com/img2.png)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/img2.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_mixed_content(self):
        text = "This is **bold**, _italic_, and `code` with a ![image](https://example.com/image.png) and a [link](https://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with a ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_unclosed_delimiter(self):
        text = "This is **bold and _italic text."
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertTrue("Closing delimiter not found" in str(context.exception))

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
