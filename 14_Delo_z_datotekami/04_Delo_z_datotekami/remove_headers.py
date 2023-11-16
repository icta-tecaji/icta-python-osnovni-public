from pathlib import Path
from itertools import dropwhile


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def header_remover(input_path: str, output_path: str) -> None:
    with open(input_path, "r") as input, open(output_path, "w") as output:
        for line in dropwhile(lambda line: line.startswith("#"), input):
            output.write(line)


if __name__ == "__main__":
    input_file = get_absolute_file_path("data/userdb.txt")
    output_file = get_absolute_file_path("data/userdb_clean.txt")
    header_remover(input_file, output_file)
