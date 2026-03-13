import unittest
from helpers import text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
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
            split_nodes_delimiter([node], "HELLO", TextType.CODE)

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

class TestExtraction(unittest.TestCase):
    def test_extract_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is a link to my [website](https://mattisbeck.com)"
        )
        self.assertListEqual([("website", "https://mattisbeck.com")], matches)

    def test_extract_invalid_image(self):
        matches = extract_markdown_images(
            "This is text with an invalid ![image]https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_invalid_links(self):
        matches = extract_markdown_links(
            "This is text with an invalid [link]https://mattisbeck.com"
        )
        self.assertListEqual([], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
        "![first](url1) and ![second](url2)"
        )
        self.assertListEqual([("first", "url1"), ("second", "url2")], matches)

    def test_empty_alt_text(self):
        matches = extract_markdown_images(
            "this image has no ![](https://link.de) alt text"
        )
        self.assertListEqual([("", "https://link.de")], matches)

    def test_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

class TestSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_images_no_image(self):
        node = TextNode(
            "This has no image",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This has no image", TextType.TEXT)
            ]
        )

    def test_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at start",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at start", TextType.TEXT),
            ]
        )

    def test_image_at_end(self):
        node = TextNode(
            "Image at the end ![image](https://i.imgur.com/zjjcJKZ.png)" ,
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Image at the end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        )

    def test_multiple_image_nodes(self):
        node = TextNode(
            "Image at the end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Image at the end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]
        )

    def test_empty_input_list(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual(new_nodes, [])

    def test_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example.com/another"),
            ]
        )

    def test_link_at_start(self):
        node = TextNode(
            "[link](https://www.example.com) at start",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" at start", TextType.TEXT),
            ]
        )

    def test_link_at_end(self):
        node = TextNode(
            "Link at the end [link](https://www.example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Link at the end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ]
        )

    def test_multiple_link_nodes(self):
        node = TextNode(
            "Link at the end [link](https://www.example.com)",
            TextType.TEXT
        )
        node2 = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Link at the end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example.com/another"),
            ]
        )

    def test_only_link(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ]
        )

    def test_no_links(self):
        node = TextNode("Just plain text no links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Just plain text no links here.", TextType.TEXT),
            ]
        )

    def test_image_syntax_is_not_a_link(self):

        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://mattisbeck.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://mattisbeck.com"),
            ]
        )

    def test_text_to_textnodes_plain_text(self):
        text = "Just plain text."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Just plain text.", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_only_bold(self):
        text = "**bold**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_multiple_same_type(self):
        text = "A **bold** and **strong** text."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("strong", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_image_and_link_order(self):
        text = "![alt](https://img.test/a.png) then [site](https://example.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("alt", TextType.IMAGE, "https://img.test/a.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ]
        )

    def test_text_to_textnodes_unclosed_delimiter_raises(self):
        text = "This has **broken markdown"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)
