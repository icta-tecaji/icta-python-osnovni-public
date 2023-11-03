import json
from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


def read_file(file_path: str) -> str:
    with open(file_path, mode="rt") as my_file:
        data = my_file.read()
    return data


if __name__ == "__main__":
    raw_file_path = get_absolute_file_path("nodes.txt")
    raw_data = read_file(raw_file_path)

    data_no_headers = ""
    # loopamo po posameznih vrsticah v datoteki
    for line in raw_data.splitlines():
        if not line.startswith("/*"):
            data_no_headers += f"{line}\n"

    data_splited = data_no_headers.split("\n\n")
    data_splited = [line.replace("ISODate(", "") for line in data_splited]
    data_splited = [line.replace(")", "") for line in data_splited]
    naprave = [json.loads(line) for line in data_splited]

    naprave_clean = []

    for naprava in naprave:
        naprava_id = naprava.get("_id", None)
        naprava_model = naprava.get("model", None)
        naprava_factoryResetCounter = naprava.get("factoryResetCounter", None)

        if naprava_model == "RAC2V1S":
            naprave_clean.append(
                {
                    "_id": naprava_id,
                    "model": naprava_model,
                    "factoryResetCounter": naprava_factoryResetCounter,
                }
            )

    print(naprave_clean)
