from website import copy_from_to
import os


def main():
    print(os.getcwd())
    copy_from_to("../static", "../public")

if __name__ == "__main__":
    main()