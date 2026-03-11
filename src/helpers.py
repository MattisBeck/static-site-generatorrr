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
    if delimiter not in ["*", "**", "_", "`"]:
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