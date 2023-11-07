# import sys
from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def get_longest_word(file_path) -> List[str]:
    with open(file_path, "r") as infile:
        words = infile.read().split()
    max_len = len(max(words, key=len))
    return list(set([word for word in words if len(word) == max_len]))


if __name__ == "__main__":
    path = "data/test.txt"
    # path = sys.argv[1]
    full_path = get_absolute_file_path(path)
    words = get_longest_word(path)
    print(f"Najdaljše besede: {', '.join(words)}")
