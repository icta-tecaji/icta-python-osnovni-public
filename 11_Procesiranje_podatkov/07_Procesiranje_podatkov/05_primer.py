import ipaddress
from collections import Counter
from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def is_ip_private(ip: str) -> bool:
    ip_object = ipaddress.ip_address(ip)
    return ip_object.is_private and not ip_object.is_reserved and not ip_object.is_loopback


if __name__ == "__main__":
    path = get_absolute_file_path("data/example_log.txt")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    status_codes = [int(log.split()[8]) for log in lines if is_ip_private(log.split()[0])]
    status_codes_counter = Counter(status_codes)
    counter = status_codes_counter.most_common()

    for code, count in counter:
        print(f"Status code: {code} -> {count}")
