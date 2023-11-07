import json
from pathlib import Path
from typing import Dict, List


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def read_data(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def write_log_report(path: str, data: List) -> None:
    with open(path, "w", encoding="utf-8") as f:
        write_values = {}
        for id, line in enumerate(data):
            write_values[id] = {"dn": line[0], "speed": line[1], "mtu": line[2]}
        json.dump(write_values, f)


if __name__ == "__main__":
    path = "data/exer1-interface-data.json"
    path = get_absolute_file_path(path)
    data = read_data(path)

    podatki = data["imdata"]
    clean_data = []
    for interface in podatki:
        attributes = interface["l1PhysIf"]["attributes"]

        dn = attributes["dn"]
        speed = attributes["speed"]
        mtu = attributes["mtu"]
        clean_data.append((dn, speed, mtu))

    write_log_report(get_absolute_file_path("data/report-interface.json"), clean_data)
