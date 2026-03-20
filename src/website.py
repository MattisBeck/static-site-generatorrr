import os
import shutil
def copy_from_to(src, dst):
    # check if current directories exists
    if not os.path.exists(src):
        raise FileNotFoundError(f"source:{src} does not exist")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    # remove everything from current dst
    os.mkdir(dst)
    files_in_src = os.listdir(src)
    for element in files_in_src:
        full_src_path = os.path.join(src, element)
        full_dst_path = os.path.join(dst, element)
        if os.path.isfile(full_src_path):
            shutil.copy(full_src_path, full_dst_path)
        elif os.path.isdir(full_src_path):
            copy_from_to(full_src_path, full_dst_path)