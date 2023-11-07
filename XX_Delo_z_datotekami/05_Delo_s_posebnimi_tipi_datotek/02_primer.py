import json
from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def serialize_python_object_to_json_string():
    data = {
        "temperature": [23.4, 54.6, 67.8, 76, 55.7, 67, 322.233],
        "wind": (12, 3, 4, 55, 6, 7, 7, 8),
        "remote": True,
        "location": "Ljubljana",
        "is_up": None,
    }
    json_formatted_string = json.dumps(data)
    print(json_formatted_string)


def deserialize_json_strin_to_python_object():
    my_string = '{"temperature": [23.4, 54.6, 67.8, 76, 55.7, 67, 322.233], "wind": [12, 3, 4, 55, 6, 7, 7, 8], "remote": true, "location": "Ljubljana", "is_up": null}'
    my_data = json.loads(my_string)
    print(my_data)


def read_json(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(data)


def write_json(path: str) -> None:
    my_string = '{"temperature": [23.4, 54.6, 67.8, 76, 55.7, 67, 322.233], "wind": [12, 3, 4, 55, 6, 7, 7, 8], "remote": true, "location": "Ljubljana", "is_up": null}'
    with open(path, "w", encoding="utf-8") as f:
        json.dump(my_string, f)


if __name__ == "__main__":
    path = "data/hrdata.json"
    path = get_absolute_file_path(path)

    # serialize_python_object_to_json_string()
    # deserialize_json_strin_to_python_object()
    # read_json(path)

    path = "data/moji_novi_podatki.json"
    path = get_absolute_file_path(path)
    write_json(path)
