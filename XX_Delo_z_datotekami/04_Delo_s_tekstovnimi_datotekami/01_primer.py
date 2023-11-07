from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


if __name__ == "__main__":
    path = "data/test.txt"
    full_path = get_absolute_file_path(path)
    with open(full_path) as reader:
        print(reader)

    print("Konec")
