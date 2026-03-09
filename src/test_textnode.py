import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an other node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.mattisbeck.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.mattisbeckt.com")
        self.assertNotEqual(node, node2)

    def test_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props={
        "href": "https://www.mattisbeck.com",
        "target": "_blank"
    })
        props_to_html = node.props_to_html()
        self.assertEqual(props_to_html,' href="https://www.mattisbeck.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="a", props={
        "href": "https://www.google.com",
        "target": "_blank"})
        repr_node = repr(node)
        self.assertEqual(repr_node, "HTMLNode(a, None, None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def props_no_props(self):
        node = HTMLNode(tag="a")
        props_to_html = node.props_to_html()
        self.assertEqual(props_to_html, "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_link_display(self):
        node = LeafNode("a", "This is a link", props={
        "href": "https://www.mattisbeck.com",
        })
        self.assertEqual(node.to_html(), '<a href="https://www.mattisbeck.com">This is a link</a>')

    def test_link_with_no_link(self):
        node = LeafNode("a", "This is a link")
        self.assertEqual(node.to_html(), '<a>This is a link</a>')

    def test_with_link_empty_dictionary(self):
        node = LeafNode("a", "This is a link", props={})
        self.assertEqual(node.to_html(), '<a>This is a link</a>')

    def test_no_tag(self):
        node = LeafNode(None, "This is valid")
        self.assertEqual(node.to_html(), 'This is valid')

    def test_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()