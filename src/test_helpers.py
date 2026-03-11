import unittest
from helpers import text_node_to_html_node, split_nodes_delimiter
from textnode import TextType, TextNode

class TestConvert(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, "https://upload.wikimedia.org/wikipedia/commons/5/54/Bg-easter-eggs.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://upload.wikimedia.org/wikipedia/commons/5/54/Bg-easter-eggs.jpg", "alt":"This is alt text" })

    def test_invalid_type(self):
        node = TextNode("some text", TextType.TEXT)
        node.text_type = "not_a_valid_type"
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
])

    def test_multiple_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_invalid_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "FFAF", TextType.CODE)

    def test_non_text_node(self):
        node = TextNode("This is a _already italic_ text", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is a _already italic_ text", TextType.ITALIC)])

    def test_unclosed_delimiter(self):
        node = TextNode("This block **has a unclosed delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.ITALIC)

    def test_delimiter_start(self):
        node =  TextNode("`This` starts with code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.TEXT),
            TextNode("This", TextType.CODE),
            TextNode(" starts with code", TextType.TEXT),
        ])

    def test_delimiter_end(self):
        node = TextNode("This ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT)
        ])

    def test_multiple_marked_up_sections(self):
        node = TextNode("**This** has multiple **bold** parts", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" has multiple ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" parts", TextType.TEXT),
        ])