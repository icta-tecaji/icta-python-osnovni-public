import os
from collections import Counter
from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def writing_to_a_file_that_doesnt_exist_x_option(path: str) -> None:
    with open(path, "x") as file:
        file.write("Test123")


def writing_to_a_file_that_doesnt_exist_path_option(path: str) -> None:
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write("Test123")
    else:
        print("File already exists!")


def append_to_file(path: str) -> None:
    with open(path, "a") as file:
        file.write("\nNova vrstica")


def working_with_multiple_files(path_read: str, path_write: str) -> None:
    with open(path_read, "r") as reader, open(path_write, "w") as writer:
        data = reader.read()
        write_data = data.upper()
        writer.write(write_data)


def is_word_in_file(path: str, search_word: str) -> bool:
    with open(path, "r") as file:
        if search_word in file.read():
            return True
        else:
            return False


def count_words_in_text_file(path: str) -> List:
    with open(path, "r", encoding="utf-8") as reader:
        text = reader.read()

    text_splited_clean = []
    text_splited = text.split()

    for word in text_splited:
        word = word.lower().strip()
        text_splited_clean.append(word)

    text_splited_clean_alpha = []
    for word in text_splited_clean:
        clean_word = []
        for letter in word:
            if letter.isalnum():
                clean_word.append(letter)
        text_splited_clean_alpha.append("".join(clean_word))

    word_count = Counter(text_splited_clean_alpha).most_common(10)
    return word_count


def get_number_of_lines(path) -> int:
    with open(path) as f:
        i = 0
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":
    # path = "data/test1.txt"
    # path = get_absolute_file_path(path)
    # # writing_to_a_file_that_doesnt_exist_x_option(path)
    # # writing_to_a_file_that_doesnt_exist_path_option(path)
    # # append_to_file(path)
    # # working_with_multiple_files(path, get_absolute_file_path("data/test2.txt"))
    # is_in_file = is_word_in_file(path, "vrstica")
    # print(is_in_file)

    path = "data/search_file.txt"
    path = get_absolute_file_path(path)
    # most_common_words = count_words_in_text_file(path)
    # print(most_common_words)

    num_of_lines = get_number_of_lines(path)
    print(f"Datoteka vsebuje {num_of_lines} vrstic.")
