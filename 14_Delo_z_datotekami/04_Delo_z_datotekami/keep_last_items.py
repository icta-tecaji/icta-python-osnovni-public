from collections import deque
from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def search(lines, pattern, history):
    prevoius_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, prevoius_lines
        prevoius_lines.append(line)


def keep_last_n(file_path: str, history_n: int = 5):
    with open(file_path, "r") as infile:
        for line, prev_lines in search(
            infile, "/bootstrap-3.3.7/js/bootstrap.min.js HTTP/1.1,304", history_n
        ):
            for pline in prev_lines:
                print(pline, end="")
            print(line, end="")
            print("-" * 25)


if __name__ == "__main__":
    path = "data/weblog.csv"
    full_path = get_absolute_file_path(path)
    keep_last_n(full_path, 7)
