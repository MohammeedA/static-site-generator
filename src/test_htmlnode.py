import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.empty_node = HTMLNode()
        self.full_node = HTMLNode(
            tag="div",
            value="test content",
            children=["child1", "child2"],
            props={"class": "test-class", "id": "test-id"}
        )

    def test_init_with_defaults(self):
        self.assertIsNone(self.empty_node.tag)
        self.assertIsNone(self.empty_node.value)
        self.assertIsNone(self.empty_node.children)
        self.assertIsNone(self.empty_node.props)

    def test_init_with_values(self):
        self.assertEqual(self.full_node.tag, "div")
        self.assertEqual(self.full_node.value, "test content")
        self.assertEqual(self.full_node.children, ["child1", "child2"])
        self.assertEqual(self.full_node.props, {"class": "test-class", "id": "test-id"})

    def test_props_to_html_none(self):
        self.assertEqual(self.empty_node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "single"})
        self.assertEqual(node.props_to_html(), 'class="single"')

    def test_props_to_html_multiple_props(self):
        result = self.full_node.props_to_html()
        self.assertIn('class="test-class"', result)
        self.assertIn('id="test-id"', result)
        self.assertEqual(len(result.split()), 2)

    def test_props_to_html_special_characters(self):
        node = HTMLNode(props={"data-test": "value&<>"})
        self.assertEqual(node.props_to_html(), 'data-test="value&<>"')

    def test_to_html_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.empty_node.to_html()
        with self.assertRaises(NotImplementedError):
            self.full_node.to_html()

    def test_repr_empty_node(self):
        expected = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(repr(self.empty_node), expected)

    def test_repr_full_node(self):
        expected = 'HTMLNode(tag=div, value=test content, children=[\'child1\', \'child2\'], props={\'class\': \'test-class\', \'id\': \'test-id\'})'
        self.assertEqual(repr(self.full_node), expected)

if __name__ == '__main__':
    unittest.main()