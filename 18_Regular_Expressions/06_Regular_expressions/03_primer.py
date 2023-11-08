import re
from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def get_robot_values(data: str):
    # @robot3!, @robot5& and @robot7#
    pattern = r"@robot\d\W"
    res = re.findall(pattern, data)
    return res


def find_values(data: str):
    pattern1 = r"User_mentions:\d"
    pattern2 = r"likes:\s\d"
    pattern3 = r"number\sof\sretweets:\s\d"

    print(re.findall(pattern1, data))
    print(re.findall(pattern2, data))
    print(re.findall(pattern3, data))


def validate_password(password: str) -> bool:
    match = re.match(r"\w{8}\d{4}", password)
    if match:
        return True
    else:
        return False


def find_all_links(data: str) -> List:
    pattern = r"http\S+"
    urls = re.findall(pattern, data)
    return urls


def email_extractor(data: str) -> List:
    pattern = r"[A-Za-z-0-9!#%&*$~.]+@\w+\.com"
    emails = re.findall(pattern, data)
    return emails


if __name__ == "__main__":
    path = get_absolute_file_path("data/short_tweets.csv")
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    # values = get_robot_values(data)
    # print(f"Robot values: {values}")

    # find_values(data)

    # password = "password1234"
    # print(f"Is validated: {validate_password(password)}")

    # urls = find_all_links(data)
    # print(urls)

    emails = email_extractor(data)
    print(emails)
