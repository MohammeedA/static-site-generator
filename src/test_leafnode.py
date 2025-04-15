import unittest
from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_no_props(self):
        node = LeafNode(tag="p", value="This is a leaf node")
        self.assertEqual(node.to_html(), "<p>This is a leaf node</p>")

    def test_leafnode_with_props(self):
        node = LeafNode(tag="a", value="Click me", props={"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click me</a>')

    def test_leafnode_no_tag(self):
        node = LeafNode(tag=None, value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leafnode_none_value(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()