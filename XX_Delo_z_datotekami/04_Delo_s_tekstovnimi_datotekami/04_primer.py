from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def reverse_file(path: str) -> None:
    with open(path, "r", encoding="utf-8") as reader:
        lines = reader.readlines()

    reversed_lines = lines[::-1]

    new_file_path = get_absolute_file_path("data/test_reversed.txt")
    with open(new_file_path, "w", encoding="utf-8") as writer:
        writer.writelines(reversed_lines)


if __name__ == "__main__":
    path = "data/test.txt"
    path = get_absolute_file_path(path)
    reverse_file(path)
    print("Konec.")
