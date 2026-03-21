from website import copy_from_to, generate_pages_recursive
import os


def main():
    print(os.getcwd())
    copy_from_to("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()