import re
from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node:TextNode):
    if not isinstance(text_node, TextNode):
        raise TypeError("text_node must be TextNode")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt" : text_node.text})
        case _:
            raise ValueError("text_node has invalid text_type")

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type):
    new_nodes = []
    if delimiter not in ["**", "_", "`"]:
        raise ValueError("invalid delimiter")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_node = node.text
        split_text_node = text_node.split(delimiter)
        # even indices are plain text
        # even lengths are invalid because they do not have a closing tag
        if len(split_text_node) % 2 == 0:
            raise ValueError("invalid markdown provided")
        for part_index in range(len(split_text_node)):
            if part_index % 2 == 0:
                new_nodes.append(TextNode(split_text_node[part_index], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text_node[part_index], text_type))
    return new_nodes

def extract_markdown_images(text) -> list[tuple[[str], [str]]]:
    # very readable
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)

def extract_markdown_links(text) -> list[tuple[[str], [str]]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        # extract image link is possible
        images = extract_markdown_images(node_text)
        # if there are no images, just return the node unchanged
        if len(images) == 0:
            new_nodes.append(node)
            continue
        # Split by all image occurrences
        before = node_text
        for alt, link in images:
            sections = before.split(f"![{alt}]({link})", 1) # index 0: everything before the image, index 1: everything after:
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            # Split everything after the first link again
            before = sections[1]
        if before != "":
            new_nodes.append(TextNode(before, TextType.TEXT))
        # append everything after the last link so that it doesn't go missing

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        links = extract_markdown_links(node_text)
        # if there are no images, just return the node unchanged
        if len(links) == 0:
            new_nodes.append(node)
            continue
        # Split by all image occurrences
        before = node_text
        for a, url in links:
            sections = before.split(f"[{a}]({url})",
                                    1)  # index 0: everything before the image, index 1: everything after:
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(a, TextType.LINK, url))
            # Split everything after the first link again
            before = sections[1]
        if before != "":
            new_nodes.append(TextNode(before, TextType.TEXT))
        # append everything after the last link so that it doesn't go missing

    return new_nodes

def text_to_textnodes(text:str) -> list[TextNode]:
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(text:str) -> list[str]:
    text_by_blocks = text.split("\n\n")
    clean_blocks = []
    for block in text_by_blocks:
        block = block.strip()
        if len(block) == 0:
            continue
        clean_blocks.append(block) # append blocks without whitespace
    return clean_blocks