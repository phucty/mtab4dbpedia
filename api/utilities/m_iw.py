import csv
import fnmatch
import os
import pickle
import zlib

import numpy as np
import texttable as tt
import logging


def create_dir(file_dir):
    """Create a directory

    Args:
        file_dir (str): file directory
    """
    folder_dir = os.path.dirname(file_dir)
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)


def load_object_csv(file_name, encoding="utf8"):
    content = []
    if os.path.exists(file_name):
        with open(file_name, "r", encoding=encoding, errors="ignore") as f:
            reader = csv.reader(f, delimiter=",")
            for r in reader:
                row_norm = []
                for c in r:
                    row_norm.append(c)
                content.append(row_norm)
    return content


def save_object_csv(file_name, rows):
    create_dir(file_name)
    temp_file = "%s.temp" % file_name
    with open(temp_file, "w") as f:
        try:
            writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            for r in rows:
                if (
                    isinstance(r, list)
                    or isinstance(r, tuple)
                    or isinstance(r, np.ndarray)
                ):
                    writer.writerow(r)
                else:
                    writer.writerow([r])
        except Exception as message:
            print(message)
    if os.path.exists(file_name):
        os.remove(file_name)
    os.rename(temp_file, file_name)


def get_files_from_dir_subdir(folder_path, extension="*"):
    all_files = []
    for root, _, file_dirs in os.walk(folder_path):
        for file_dir in fnmatch.filter(file_dirs, "*.%s" % extension):
            if ".DS_Store" not in file_dir:
                all_files.append(os.path.join(root, file_dir))
    return all_files


def get_files_from_dir(
    folder_path, extension="*", limit_reader=-1, is_sort=False, reverse=False
):
    all_file_dirs = get_files_from_dir_subdir(folder_path, extension)

    if is_sort:
        file_with_size = [(f, os.path.getsize(f)) for f in all_file_dirs]
        file_with_size.sort(key=lambda f: f[1], reverse=reverse)
        all_file_dirs = [f for f, _ in file_with_size]
    if limit_reader < 0:

        limit_reader = len(all_file_dirs)
    return all_file_dirs[:limit_reader]


def print_table(cell_values, n_col=-1, max_row=0):
    if n_col == -1:
        n_col = max(len(r) for r in cell_values)
    max_row = len(cell_values) if max_row <= 0 else max_row
    tab = tt.Texttable(max_width=0)  # max_width=300
    tab.add_row([""] + [_r for _r in range(n_col)])
    for r_i, r in enumerate(cell_values[:max_row]):
        if len(r) < n_col:
            r += ["" for i in range(n_col - len(r))]
        r = [str(r_i)] + r
        tab.add_row(r)

    try:
        log_message = tab.draw()
    except Exception as messageException:
        log_message = messageException
    return log_message


def print_status(message, is_screen=True, is_log=True) -> object:
    if is_screen:
        print(message)
    if is_log:
        logging.info(message)


def save_obj_pkl(file_name, save_object, is_compress=False, is_message=True):
    create_dir(file_name)
    save_file = file_name
    if ".pkl" not in file_name:
        save_file = file_name + ".pkl"
    if is_compress and ".zlib" not in file_name:
        save_file += ".zlib"

    temp_file = save_file + ".temp"

    # Write temp
    with open(temp_file, "wb") as fp:
        if is_compress:
            save_data = zlib.compress(
                pickle.dumps(save_object, pickle.HIGHEST_PROTOCOL)
            )
            fp.write(save_data)
        else:
            pickle.dump(save_object, fp, pickle.HIGHEST_PROTOCOL)

    try:
        if os.path.exists(save_file):
            os.remove(save_file)
    except Exception as message:
        print_status(message)

    os.rename(temp_file, save_file)
    if is_message:
        print_status("Saved: - %d - %s" % (len(save_object), save_file), is_log=False)
    return save_file


def load_obj_pkl(file_name, is_message=False, is_compress=False):
    load_obj = None
    if not os.path.exists(file_name) and ".pkl" not in file_name:
        file_name = file_name + ".pkl"

    if not os.path.exists(file_name) and ".zlib" not in file_name:
        file_name = file_name + ".zlib"
    with open(file_name, "rb") as fp:
        if is_compress or ".zlib" in file_name:
            load_obj = pickle.loads(zlib.decompress(fp.read()))
        else:
            load_obj = pickle.load(fp)
    if is_message and load_obj:
        print_status("%d loaded items - %s" % (len(load_obj), file_name))
    return load_obj
