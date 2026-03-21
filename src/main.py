from website import copy_from_to, generate_page
import os


def main():
    print(os.getcwd())
    copy_from_to("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()