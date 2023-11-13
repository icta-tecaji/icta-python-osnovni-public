import bz2
import fnmatch
import gzip
import os
import re
import sys
from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def gen_find_files(main_path: str, file_filter_string: str):
    for path, dir_list, file_list in os.walk(main_path):
        for file in fnmatch.filter(file_list, file_filter_string):
            yield os.path.join(path, file)


def gen_opener(filenames):
    for filename in filenames:
        if filename.endswith(".gz"):
            f = gzip.open(filename, "rt")
        elif filename.endswith(".bz2"):
            f = bz2.open(filename, "rt")
        else:
            f = open(filename, "rt")
        yield f
        f.close()


def gen_concatenate(iterators):
    for it in iterators:
        yield from it


def gen_grep(pattern: str, lines):
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main_folder_name = "pipeline"
        file_filter = "access-log-*"
        user_filter = r"robotsl?.txt"
    elif len(sys.argv) == 4:
        main_folder_name = sys.argv[1]
        file_filter = sys.argv[2]
        user_filter = sys.argv[3]
    else:
        print("Preveri število argumentov!")
        sys.exit(1)

    main_data_folder = get_absolute_file_path(main_folder_name)

    lognames = gen_find_files(main_data_folder, file_filter)
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    filtered_lines = gen_grep(user_filter, lines)

    for line in filtered_lines:
        print(line, end="")
