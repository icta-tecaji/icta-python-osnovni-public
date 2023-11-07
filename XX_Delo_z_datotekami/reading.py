from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def read_file(file_path: str) -> str:
    with open(file_path, mode="rt") as my_file:
        data = my_file.read()
    return data


def read_file_options(file_path: str) -> None:
    with open(file_path, mode="rt") as my_file:
        data = my_file.read(45)
        print(f"Part1: {data}")
        data = my_file.read(20)
        print(f"Part2: {data}")


def read_file_in_lines(file_path: str) -> List[str]:
    with open(file_path, mode="rt") as my_file:
        data = my_file.readlines()
    return data


if __name__ == "__main__":
    path = "data/logs_small.txt"
    full_path = get_absolute_file_path(path)

    # logs = read_file(full_path)
    # print(logs[:200])

    # read_file_options(full_path)

    data = read_file_in_lines(full_path)
    for line in data:
        print(line, end="\n\n")
