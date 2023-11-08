import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def read_log_file(path: str) -> List:
    with open(path, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=",")
        line_count = 0
        data = []
        for row in csv_reader:
            if line_count == 0:
                header = row
                line_count += 1
            else:
                data.append(row)
                line_count += 1

    print(f"Uspešno prebrana datoteka {path}. Vrstice: {line_count}\nHeader: {header}")
    return data


def transform_timestamp(old_timestamp: str) -> str:
    # preoblikujemo v timedate objekt
    time_object = datetime.strptime(old_timestamp, "%d/%b/%Y:%H:%M:%S")
    updated_time_object = time_object + timedelta(hours=1)
    clean_data = datetime.strftime(updated_time_object, "%Y-%m-%dT%H:%M:%S")
    return clean_data


def transform_data(podatki: List[str]) -> List:
    clean_data = []
    for line in podatki:
        ip = line[0]
        time = transform_timestamp(line[1].replace("[", ""))
        method = line[2].split()[0]
        url = line[2].split()[1]
        protocol = line[2].split()[2]
        status_code = int(line[3])
        new_log = [ip, time, method, url, protocol, status_code]
        clean_data.append(new_log)
    return clean_data


def write_to_csv(path: str, podatki: List) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["IP", "Time", "Method", "URL", "Protocol", "Status Code"])
        writer.writerows(podatki)


if __name__ == "__main__":
    path = "data/weblog.csv"
    path = get_absolute_file_path(path)
    podatki = read_log_file(path)
    urejeni_podatki = transform_data(podatki)
    path = "data/weblog_urejeni.csv"
    path = get_absolute_file_path(path)
    write_to_csv(path, urejeni_podatki)
