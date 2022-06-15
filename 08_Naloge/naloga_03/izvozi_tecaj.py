import sys
import os
from pathlib import Path
from typing import Dict, List
import requests
import json


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def validate_year_int(year: int) -> bool:
    try:
        year_data = int(year)
        # preverimo če je int med 2005 in 2021
        if year_data >= 2005 and year_data <= 2021:
            return True
        else:
            return False
    except ValueError:
        return False


def validate_year(year_data: str) -> bool:
    if "-" in year_data:
        start_year = year_data.split("-")[0]
        end_year = year_data.split("-")[1]
        if not all([validate_year_int(start_year), validate_year_int(end_year)]):
            return False

        if start_year < end_year:
            return True
        else:
            return False
    else:
        return validate_year_int(year_data)


def select_years(year_data) -> List[int]:
    if "-" in year_data:
        start_year = int(year_data.split("-")[0])
        end_year = int(year_data.split("-")[1])
    else:
        start_year = int(year_data)
        end_year = start_year

    return [year for year in range(start_year, end_year + 1)]


def get_exchange_data(year: int) -> Dict:
    url = f"https://api.frankfurter.app/{year}-01-01..{year}-12-31"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def parse_data_and_save_to_json(data, data_folder) -> None:
    data = data["rates"]
    for date, exchanges in data.items():
        year = date.split("-")[0]
        month = date.split("-")[1]
        os.makedirs(os.path.join(data_folder, str(year)), exist_ok=True)

        with open(
            os.path.join(data_folder, str(year), f"mt_{month}_{year}.json"), "a"
        ) as f:
            write_data = f"{date}: {exchanges}"
            json.dump(write_data, f)
            f.write("\n")


if __name__ == "__main__":
    MAIN_DATA_FOLDER = get_absolute_file_path("menjalni_tecaj_podatki")

    # 1. pridobimo prvi parameter iz argumenta skripte ob zagonu če obstaja
    try:
        leto = sys.argv[1]
    except IndexError:
        print("Leto ni bilo nastavjeno.")
        leto = input("Prosimo vstavite letnico v obliki npr. 2020 ali 2012-2017: ")

    # validacija podatka
    if not validate_year(leto):
        print("Vnešeno leto je napačno! Exit...")
        sys.exit(1)

    # izvozimo list let
    years = select_years(leto)
    # ustvarimo glavno mapo če ne obstaja
    os.makedirs(MAIN_DATA_FOLDER, exist_ok=True)

    for year in years:
        print(f"Pridobivanje podatkov za leto {year}.")
        year_data = get_exchange_data(year)
        parse_data_and_save_to_json(year_data, MAIN_DATA_FOLDER)
