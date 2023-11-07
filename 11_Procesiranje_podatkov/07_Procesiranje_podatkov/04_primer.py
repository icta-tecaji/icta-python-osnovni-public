from functools import reduce
from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def analyze_with_functions(data: List[str]):
    ip_addresses = list(map(lambda x: x.split()[0], data))
    filtered_ips = list(filter(lambda x: int(x.split(".")[0]) <= 20, ip_addresses))
    count_all = reduce(lambda x, _: 2 if isinstance(x, str) else x + 1, ip_addresses)
    count_filtered = reduce(lambda x, _: 2 if isinstance(x, str) else x + 1, filtered_ips)
    ratio = count_filtered / count_all
    print(round(ratio * 100, 2))


def analyze_with_comprehations(data: List[str]):
    ip_addresses = [line.split()[0] for line in data]
    filtered_ips = [ip for ip in ip_addresses if int(ip.split(".")[0]) <= 20]
    count_all = len(ip_addresses)
    count_filtered = len(filtered_ips)
    ratio = count_filtered / count_all
    print(round(ratio * 100, 2))


if __name__ == "__main__":
    path = get_absolute_file_path("data/example_log.txt")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    analyze_with_functions(lines)
    analyze_with_comprehations(lines)
