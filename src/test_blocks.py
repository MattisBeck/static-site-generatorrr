import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


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
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_cleaning_of_whitespaces(self):
        md = """
This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_triple_newline(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
            """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_only_newlines(self):
        md = """






            """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
            ],
        )

    def test_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        md = "### This is a valid heading"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.HEADING
        )

    def test_heading_no_whitespace(self):
        md = "###This is an invalid heading"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_heading_no_following_characters(self):
        md = "### "
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_heading_no_following_characters2(self):
        md = "###"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_heading_too_many_hashtags(self):
        md = "#######"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH,
        )

    def test_heading_wrong_hashtag(self):
        md = "###*# This is invalid"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH,
        )

    def test_codeblock(self):
        md = ("""```
This is valid code
```""")
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.CODE
        )
    def test_codeblock_no_newline(self):
        md = """``` This is invalid code ```"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_codeblock_no_closing_quote(self):
        md = ("""```
This is invalid code
`
""")
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_quoteblock(self):
        md = "> This is a deep quote"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.QUOTE
        )

    def test_quoteblock2(self):
        md = ">This also a deep quote"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.QUOTE
        )

    def test_quoteblock_whitespace(self):
        md = " > This isn't a deep quote"
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_unordered_list(self):
        md = """- Type 1
- Type 2
- Type 3
- Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list_no_whitespace(self):
        md = """-Type 1
-Type 2
-Type 3
-Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_unordered_list_no_newline(self):
        md = """- Type 1 - Type 2"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list_wrong_starts(self):
        md = """- Type 1
        2. Type 2
        3. Type 3
        4. Type 4
                """
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_ordered_list(self):
        md = """1. Type 1
2. Type 2
3. Type 3
4. Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.ORDERED_LIST
        )

    def test_ordered_list_no_whitespace(self):
        md = """1.Type 1
2.Type 2
3.Type 3
4.Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_ordered_list_wrong_number_sequence(self):
        md = """1. Type 1
3. Type 2
4. Type 3
5. Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_ordered_list_starts_wrong(self):
        md = """2. Type 1
3. Type 2
4. Type 3
5. Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_ordered_list_mixed_markers(self):
        md = """1. Type 1
- Type 2
3. Type 3
4. Type 4"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.PARAGRAPH
        )

    def test_ordered_list_single_item(self):
        md = """1. Only item"""
        markdown_type = block_to_block_type(md)
        self.assertEqual(
            markdown_type,
            BlockType.ORDERED_LIST
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
    # This is a **bold** heading

    ## This is a _italic_ subheading
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bold</b> heading</h1><h2>This is a <i>italic</i> subheading</h2></div>",
        )

    def test_quote(self):
        md = """
    > This is a **blockquote** with inline stuff
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>blockquote</b> with inline stuff</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
    - This is the **first** item
    - This is the _second_ item
    - This is the third item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the <b>first</b> item</li><li>This is the <i>second</i> item</li><li>This is the third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. First item with `code`
    2. Second item with **bold**
    3. Third item plain
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <code>code</code></li><li>Second item with <b>bold</b></li><li>Third item plain</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
    # My Document

    This is a paragraph with **bold** and _italic_ text.

    - Item one
    - Item two
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>My Document</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><ul><li>Item one</li><li>Item two</li></ul></div>",
        )

    def test_multiline_quote(self):
        md = """
    > This is the first line
    > This is the **second** line
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is the first line This is the <b>second</b> line</blockquote></div>",
        )

    def test_quote_space(self):
        md = """
    > This is a quote with a space
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with a space</blockquote></div>",
        )

    def test_heading_levels(self):
        md = """
    ### h3 heading

    #### h4 heading

    ##### h5 heading

    ###### h6 heading
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>h3 heading</h3><h4>h4 heading</h4><h5>h5 heading</h5><h6>h6 heading</h6></div>",
        )

    def test_single_item_list(self):
        md = """
    - Only one item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Only one item</li></ul></div>",
        )

    def test_single_item_ordered_list(self):
        md = """
    1. Only one item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Only one item</li></ol></div>",
        )