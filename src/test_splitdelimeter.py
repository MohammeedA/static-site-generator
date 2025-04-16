import unittest
from split_delimiter import split_nodes_delimiter
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
        print(result)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[3].text, "more bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)

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
        self.assertTrue("invalid Markdown syntax" in str(context.exception))

    def test_non_TEXT_node(self):
        node = TextNode("*already bold*", TextType.BOLD)
        nodes = [node]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "*already bold*")
        self.assertEqual(result[0].text_type, TextType.BOLD)

if __name__ == '__main__':
    unittest.main()