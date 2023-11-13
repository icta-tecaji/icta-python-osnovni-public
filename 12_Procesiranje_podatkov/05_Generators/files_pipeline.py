import bz2
import fnmatch
import gzip
import os
import re


def gen_find_files(files_prefix: str, files_top_path: str) -> str:
    for dirpath, dirnames, filenames in os.walk(files_top_path):
        for name in fnmatch.filter(filenames, files_prefix):
            yield os.path.join(dirpath, name)


def gen_file_opener(filenames):
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


def gen_filter(pattern, lines):
    re_pat = re.compile(pattern)
    for line in lines:
        if re_pat.search(line):
            yield line


if __name__ == "__main__":
    log_names = gen_find_files("access-log-*", "data/pipeline")
    log_files = gen_file_opener(log_names)
    lines = gen_concatenate(log_files)
    lines = gen_filter("robotsl?.txt", lines)

    for line in lines:
        print(line.strip())
