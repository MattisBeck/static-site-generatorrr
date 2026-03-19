from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode
from helpers import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"


def markdown_to_blocks(text:str) -> list[str]:
    text_by_blocks = text.split("\n\n")
    clean_blocks = []
    for block in text_by_blocks:
        block = "\n".join(line.strip() for line in block.split("\n"))
        block = block.strip()
        if len(block) == 0:
            continue
        clean_blocks.append(block)
    return clean_blocks

def block_to_block_type(markdown_block:str) -> BlockType:
    lines = [line for line in markdown_block.split("\n") if line]
    if markdown_block.startswith("#"):
        parts = markdown_block.split(" ", 1)
        if len(parts) < 2 or parts[1] == "":
            return BlockType.PARAGRAPH
        num_hashtags = len(parts[0])
        if 1 <= num_hashtags <= 6 and all(c == "#" for c in parts[0]):
            return BlockType.HEADING
    elif markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{index+1}. ") for index, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown:str) -> HTMLNode:
    def text_to_children(texts:str) -> list[HTMLNode]:
        """
        :param texts: Markdown text
        :return: list of leafnodes
        """
        list_textnodes = text_to_textnodes(texts)
        # convert each textnode to htmlnode
        list_of_htmlnodes = [text_node_to_html_node(textnode) for textnode in list_textnodes]
        return list_of_htmlnodes

    final_children = []
    # split Markdown into separate blocks
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(" ".join(line.strip() for line in block.split("\n")))
                new_html_node = ParentNode("p", children)
                final_children.append(new_html_node)
            case BlockType.HEADING:
                # get heading size
                for i in range(len(block)):
                    if block[i] != "#":
                        children = text_to_children(block.removeprefix(f"{i * '#'} "))
                        new_html_node = ParentNode(f"h{i}", children)
                        final_children.append(new_html_node)
                        break
            case BlockType.CODE:
                text = block.removeprefix("```\n").removesuffix("```")
                text = "\n".join(line.strip() for line in text.split("\n"))
                child = text_node_to_html_node(TextNode(text, TextType.TEXT))
                new_html_node = ParentNode("pre",[ParentNode("code", [child])])
                final_children.append(new_html_node)
            case BlockType.QUOTE:
                lines = block.split("\n")
                text = " ".join(line.removeprefix(">").strip() for line in lines)
                children = text_to_children(text)
                new_html_node = ParentNode("blockquote", children)
                final_children.append(new_html_node)
            case BlockType.UNORDERED_LIST:
                children = []
                # split lists by line
                lines = block.split("\n")
                for line in lines:
                    line = line.removeprefix("- ")
                    children_of_line = text_to_children(line)
                    children.append(ParentNode("li", children=children_of_line))
                # wrap every child inside a li element
                new_html_node = ParentNode("ul", children)
                final_children.append(new_html_node)
            case BlockType.ORDERED_LIST:
                children = []
                # split lists by line
                lines = block.split("\n")
                for index, line in enumerate(lines):
                    line = line.removeprefix(f"{index+1}. ")
                    children_of_line = text_to_children(line)
                    children.append(ParentNode("li", children=children_of_line))
                # wrap every child inside a li element
                new_html_node = ParentNode("ol", children)
                final_children.append(new_html_node)
    return ParentNode("div", final_children)