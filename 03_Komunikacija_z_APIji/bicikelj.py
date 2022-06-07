from datetime import datetime
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


def parse_station_info(bicikelj_data: Dict) -> Dict[int, Dict]:
    parsed_data = dict()
    for station_number, station_info in bicikelj_data["markers"].items():
        parsed_data[int(station_number)] = {
            "ime_postaje": station_info["name"],
            "prosta_kolesa": station_info["station"]["available"],
            "prosta_mesta": station_info["station"]["free"],
            "skupaj_mest": station_info["station"]["total"],
        }
    return parsed_data


def show_station_info(parsed_data: Dict[int, Dict], id_postaje: int):
    izbrana_postaja = parsed_data[id_postaje]
    output_string = f"""
    POSTAJA: {izbrana_postaja["ime_postaje"]}
    ŠTEVILO MEST: {izbrana_postaja["skupaj_mest"]}
    KOLESA: {izbrana_postaja["prosta_kolesa"]}
    PROSTA MESTA: {izbrana_postaja["prosta_mesta"]}

        {"* " * int(izbrana_postaja["prosta_kolesa"])} {"- " * int(izbrana_postaja["prosta_mesta"])}
    """
    print(output_string)


if __name__ == "__main__":
    data = get_bicikelj_data(BICIKELJ_URL)
    if data:
        last_update = datetime.fromtimestamp(data["updated"]).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        print(f"Data last updated at: {last_update}.")
        parsed_data = parse_station_info(data)
        print("Postje na voljo:")
        print(parsed_data)
        for id_postaje, station in parsed_data.items():
            print(f"  -->  {id_postaje}) {station['ime_postaje']}")
        id_postaje = int(input("Vnesite ID postaje: "))
        show_station_info(parsed_data, id_postaje)
    else:
        print("Skripta se ni uspešno izvedla!")
