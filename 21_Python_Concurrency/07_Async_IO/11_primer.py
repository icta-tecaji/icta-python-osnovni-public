import os
import time
from pathlib import Path

import requests


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def write_genre(file_name):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the
    name of the given file
    """

    req = requests.get(
        "https://binaryjazz.us/wp-json/genrenator/v1/genre/",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    genre = req.json()

    with open(file_name, "w") as new_file:
        print(f"Writing '{genre}' to '{file_name}'...")
        new_file.write(genre)


if __name__ == "__main__":
    path = get_absolute_file_path("sync")
    os.makedirs(path, exist_ok=True)

    print("Starting...")
    start = time.perf_counter()

    for i in range(10):
        write_genre(f"{path}/new_file{i}.txt")

    end = time.perf_counter()
    print(f"Time to complete synchronous read/writes: {round(end - start, 2)} seconds")
