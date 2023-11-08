import re
from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def string_search(
    file_path: str, iskana_beseda: str, st_prikazanih_znakov: int
) -> List[str]:
    with open(file_path, "r") as file:
        content = file.read()
        find_results_indexes = [
            m.start() for m in re.finditer(rf"{iskana_beseda}", content)
        ]
        return [
            content[index : index + st_prikazanih_znakov]
            for index in find_results_indexes
        ]


if __name__ == "__main__":
    path = "data/search_file.txt"
    # path = sys.argv[1]
    full_path = get_absolute_file_path(path)
    words = string_search(path, "Python", 20)
    print("Najdene besede:", "\n".join(words))
