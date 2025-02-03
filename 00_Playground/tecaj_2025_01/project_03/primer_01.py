"""Prvi primer obdelave podatkov."""

import time
from pathlib import Path

from loguru import logger

MERITVE_PATH_BASE = Path(__file__).parent
COLUMNS = [
    "Pt",
    "Reg",
    "Sys",
    "Mn",
    "Mv",
    "On",
    "Prc",
    "Pr",
    "Pv",
    "Sp",
    "Hs",
    "Oc",
    "Cc",
    "Ct",
    "UIt",
    "Rpid",
    "Probe",
    "Grill",
    "Steam",
    "Ntc",
    "Timestamp",
]


def parse_very_big_files() -> None:
    """Parse very big files."""
    time_start = time.time()
    file_path_raw = MERITVE_PATH_BASE / "meritve.txt"
    file_clean = MERITVE_PATH_BASE / "meritve_clean.csv"
    with file_path_raw.open("r", encoding="utf-8") as file_read, file_clean.open("w", encoding="utf-8") as file_write:
        file_write.write(",".join(COLUMNS) + "\n")
        for line in file_read:
            if line.startswith("Reg>"):
                line_parsed = line.strip().replace("Reg>MF_PY_60 V0.25 ", "").replace("  -> ", " ")
                columns = line_parsed.split(" ")
                date_row = columns[-2]
                time_row = columns[-1]
                values = [column.split(":")[1] for column in columns[:-2]]
                csv_line = ",".join(values) + f",{date_row}T{time_row}"
                file_write.write(csv_line + "\n")
            else:
                continue

    logger.info(f"[parse_very_big_files] Time elapsed: {time.time() - time_start:.4f} s.")


def parse_small_file_in_memory_python() -> None:
    """Parse small file in memory."""
    time_start = time.time()
    file_path_raw = MERITVE_PATH_BASE / "meritve.txt"
    new_rows = []
    with file_path_raw.open("r", encoding="utf-8") as file:
        lines = file.readlines()
        lines_with_measurement = [line.strip() for line in lines if line.startswith("Reg>")]
        lines_with_replacement = [line.replace("Reg>MF_PY_60 V0.25 ", "").replace("  -> ", " ") for line in lines_with_measurement]
        for line in lines_with_replacement:
            columns = line.split(" ")
            date_row = columns[-2]
            time_row = columns[-1]
            values = [column.split(":")[1] for column in columns[:-2]]
            csv_line = ",".join(values) + f",{date_row}T{time_row}"
            new_rows.append(csv_line)

    file_clean = MERITVE_PATH_BASE / "meritve_clean.csv"
    with file_clean.open("w", encoding="utf-8") as file:
        file.write(",".join(COLUMNS))
        file.write("\n")
        file.write("\n".join(new_rows))

    logger.info(f"[parse_small_file_in_memory_python] Time elapsed: {time.time() - time_start:.4f} s.")


if __name__ == "__main__":
    parse_very_big_files()
    parse_small_file_in_memory_python()
