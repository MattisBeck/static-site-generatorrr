import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()