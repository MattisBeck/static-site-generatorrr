import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><b>grandchild</b></span></div>')

    def test_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), '<div></div>')

    def test_multiple_nested_children(self):
        children = [
            LeafNode("span", "child"),
            ParentNode("div", [LeafNode("b", "grandchild")]),
            ParentNode("div", [ParentNode("span", [LeafNode("b", "Some child")])]),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(
            parent_node.to_html(),
            '<p><span>child</span><div><b>grandchild</b></div><div><span><b>Some child</b></span></div></p>'
        )

    def test_parent_class_with_props(self):
        parent_node = ParentNode("a", [LeafNode("span", "child")], props={"href": "https://www.testtest.de"})
        self.assertEqual(parent_node.to_html(), '<a href="https://www.testtest.de"><span>child</span></a>')



