from enum import Enum


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
        block = block.strip()
        if len(block) == 0:
            continue
        clean_blocks.append(block) # append blocks without whitespace
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