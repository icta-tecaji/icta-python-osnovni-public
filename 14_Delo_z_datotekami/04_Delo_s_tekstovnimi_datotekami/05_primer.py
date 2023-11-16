from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def find_longest_word_in_file(path: str) -> str:
    """
    Returns the longest word in file.
    """
    with open(path, "r", encoding="utf-8") as my_file:
        text = my_file.read()

    words = text.split()
    max_len = len(max(words, key=len))

    for word in words:
        if len(word) == max_len:
            return word


if __name__ == "__main__":
    path = "data/search_file.txt"
    path = get_absolute_file_path(path)
    longest_word = find_longest_word_in_file(path)
    print(f"Najdaljša beseda v datoteki {path} je {longest_word}.")
