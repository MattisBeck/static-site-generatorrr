from website import copy_from_to, generate_pages_recursive
import os
import sys


def main():
    basepath = sys.argv[1]
    destination = "docs"
    copy_from_to("static", destination)
    generate_pages_recursive("content", "template.html", destination, basepath)


if __name__ == "__main__":
    main()