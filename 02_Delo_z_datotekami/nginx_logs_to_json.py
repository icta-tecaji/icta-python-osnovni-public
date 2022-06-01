import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin

domain_regex = re.compile(r"https?:\/\/[\w\d\.\-]+")


def parse_timestamp_format(old_timestamp: str) -> str:
    timestamp_object = datetime.strptime(old_timestamp, "%d/%b/%Y:%H:%M:%S")
    new_timestamp = timestamp_object.strftime("%Y-%m-%dT%H:%M:%S")
    return new_timestamp


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def read_and_parse_logs(file_path: str) -> List[Dict]:
    with open(file_path, mode="rt") as my_file:
        logs: List = []
        for line in my_file.readlines():
            log = dict()
            line_splited = line.split()
            log["ip"] = line_splited[0]
            log["timestamp"] = parse_timestamp_format(line_splited[3].replace("[", ""))
            log["http_method"] = line_splited[5].strip('"')
            domain = domain_regex.search(line_splited[10].strip('"')).group(0)
            path = line_splited[6]
            log["url"] = urljoin(domain, path)
            log["status_code"] = int(line_splited[8])
            log["bytes"] = int(line_splited[9])
            log["user_agent"] = line.strip().split('"')[-2]
            logs.append(log)
    return logs


def write_to_json_file(file_path: str, data: List[Dict]) -> None:
    all_data = {"title": f"Nginx logs from {datetime.now()}", "data": data}
    with open(file_path, mode="w") as output_file:
        json.dump(all_data, output_file)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_path = sys.argv[1]
        output_path = f"{sys.argv[1].split('.')[-2]}.json"
    else:
        input_path = "data/logs_small.txt"
        output_path = "data/logs_small.json"

    print(f"Parsing {input_path} to JSON. Outuput file: {output_path}.")
    full_input_path = get_absolute_file_path(input_path)
    full_output_path = get_absolute_file_path(output_path)
    logs = read_and_parse_logs(full_input_path)
    write_to_json_file(full_output_path, logs)
    print("Parsing DONE!")
