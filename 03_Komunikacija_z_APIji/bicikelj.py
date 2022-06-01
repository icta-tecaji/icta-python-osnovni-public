from typing import Dict, Union

import requests
from requests import ConnectionError, Timeout

BICIKELJ_URL = "https://opendata.si/promet/bicikelj/list/"


def get_bicikelj_data(url: str) -> Union[Dict, None]:
    try:
        response = requests.get(url, timeout=2)
    except Timeout:
        print(f"Failed to connect to URL: {url}. Timeout!")
    except ConnectionError:
        print(f"Failed to connect to URL: {url}. Connection Error!")
    else:
        if response.status_code == 200:
            return response.json()
        else:
            print("Not found!")


if __name__ == "__main__":
    data = get_bicikelj_data(BICIKELJ_URL)
    if data:
        pass
        # nadaljuje program
        print(data)
    else:
        print("Skripta se ni uspešno izvedla!")
