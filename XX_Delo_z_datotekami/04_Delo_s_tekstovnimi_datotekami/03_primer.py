from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def transoform_file_to_upper_case(path: str) -> None:
    with open(path, "r", encoding="utf-8") as reader:
        lines = reader.readlines()

    upper_lines = []
    for line in lines:
        upper_lines.append(line.upper())

    new_file_path = get_absolute_file_path("data/test_uppper.txt")
    with open(new_file_path, "w", encoding="utf-8") as writer:
        # for line in upper_lines:
        #     writer.write(line)
        writer.writelines(upper_lines)


if __name__ == "__main__":
    path = "data/test.txt"
    path = get_absolute_file_path(path)
    transoform_file_to_upper_case(path)
