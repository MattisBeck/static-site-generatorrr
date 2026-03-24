import os
import shutil
from blocks import markdown_to_html_node
from pathlib import Path

def copy_from_to(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f"source:{src} does not exist")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for element in os.listdir(src):
        full_src_path = os.path.join(src, element)
        full_dst_path = os.path.join(dst, element)
        if os.path.isfile(full_src_path):
            shutil.copy(full_src_path, full_dst_path)
        elif os.path.isdir(full_src_path):
            copy_from_to(full_src_path, full_dst_path)

def extract_title(markdown):
    # extract first line which starts with a h1 header
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Markdown file doesnt start with a h1 heading")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r") as f:
        source = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    top_html_node = markdown_to_html_node(source)
    html = top_html_node.to_html()
    title = extract_title(source)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    destination_directories = os.path.dirname(dest_path)
    if not os.path.exists(destination_directories):
        os.makedirs(destination_directories)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_path, base_path):
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"dir_path_content:{dir_path_content} does not exist")
    for element in os.listdir(dir_path_content):
        print(f"{dir_path_content}/{element}")
        if os.path.isdir(os.path.join(dir_path_content, element)):
            generate_pages_recursive(os.path.join(dir_path_content, element), template_path, os.path.join(dest_path, element), base_path)
        else:
            destination_path = Path(os.path.join(dest_path, element)).with_suffix(".html")
            generate_page(os.path.join(dir_path_content, element), template_path, destination_path, base_path)