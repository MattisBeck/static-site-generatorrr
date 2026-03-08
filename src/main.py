from textnode import TextNode, TextType


def main():
    node = TextNode("**This is Bold**", TextType.BOLD)
    print(node)

if __name__ == "__main__":
    main()