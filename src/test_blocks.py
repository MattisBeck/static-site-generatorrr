import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType


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


