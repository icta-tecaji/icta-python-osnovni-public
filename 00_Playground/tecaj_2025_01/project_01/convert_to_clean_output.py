"""Script for converting raw data to clean data."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path

import pandas as pd
from loguru import logger
from matplotlib.figure import Figure

# Set logger configuration.
logger.remove()
logger_format = "<white>{time:YYYY-MM-DD HH:mm:ss.SSS}</white> | <level>{level: <8}</level> | <level>{message}</level>"
logger.add(sys.stderr, format=logger_format, level="DEBUG")

# Set up main variables.
ROOT_SCRIPT_PATH = Path(__file__).parent
DATA_POINT_DELIMITER = "HW_INFO ::: Parameters"
LINES_IN_DATA_POINT = 7
current_buffered_line = []


class FileTypes(Enum):
    """File types for exporting data."""

    CSV = "csv"
    JSON = "json"
    XLSX = "xlsx"


def parse_line_data(line: str) -> dict | None:
    """Parse line data."""
    line = line.strip()
    if not line:
        return None

    if DATA_POINT_DELIMITER in line:
        logger.debug(f"Found data point delimiter: {DATA_POINT_DELIMITER}")
        current_buffered_line.append(line)
    elif current_buffered_line and len(current_buffered_line) < LINES_IN_DATA_POINT:
        current_buffered_line.append(line)
    elif current_buffered_line and len(current_buffered_line) == LINES_IN_DATA_POINT:
        try:
            time_point = int(current_buffered_line[0].split(" ")[0])
            uptime_seconds = int(current_buffered_line[1].split(":")[1].strip().split(" ")[0])
            ntc_temp = (
                float(current_buffered_line[2].split(":")[1].strip().split(" ")[0]) if "-" not in current_buffered_line[2] else None
            )
            bridge_temp = float(current_buffered_line[3].split(":")[1].strip().split(" ")[0])
            target_speed_rpm = int(current_buffered_line[4].split(":")[1].strip().split(" ")[0])
            speed_rpm = int(current_buffered_line[5].split(":")[1].strip().split(" ")[0])
            motor_power_w = int(current_buffered_line[6].split(":")[1].strip().split(" ")[0])
            data_point = {
                "time_point": time_point,
                "uptime_seconds": uptime_seconds,
                "ntc_temp": ntc_temp,
                "bridge_temp": bridge_temp,
                "target_speed_rpm": target_speed_rpm,
                "speed_rpm": speed_rpm,
                "motor_power_w": motor_power_w,
            }
            current_buffered_line.clear()
        except Exception as err:  # noqa: BLE001
            logger.critical(f"Failed to parse data point: {current_buffered_line}. Error: {err}")
            sys.exit(1)
        else:
            return data_point
    return None


def parse_raw_data_to_dataframe(file_path: Path) -> pd.DataFrame:
    """Parse raw data from the file and return it as pandas DataFrame."""
    all_data = []
    with file_path.open("r") as file:
        for line in file:
            parsed_data_point = parse_line_data(line)
            if parsed_data_point:
                all_data.append(parsed_data_point)
    logger.info(f"Successfully parsed {len(all_data)} data points from the file.")
    return pd.DataFrame(all_data)


def export_data_to_file(data: pd.DataFrame, file_type: FileTypes) -> None:
    """Export data to a file."""
    if file_type == FileTypes.CSV:
        data.to_csv(ROOT_SCRIPT_PATH / "clean_data.csv", index=False)
    elif file_type == FileTypes.JSON:
        data.to_json(ROOT_SCRIPT_PATH / "clean_data.json", orient="records", index=False)
    elif file_type == FileTypes.XLSX:
        data.to_excel(ROOT_SCRIPT_PATH / "clean_data.xlsx", index=False)
    logger.success(f"Successfully exported the cleaned data to {file_type.value} file. Location: {ROOT_SCRIPT_PATH}")


def export_data_to_plot(data: pd.DataFrame) -> None:
    """Export data to a plot."""
    ax = data.plot(
        x="time_point",
        y=["bridge_temp", "speed_rpm", "motor_power_w"],
        kind="line",
        title="Bridge Temp, Speed RPM, Motor Power W",
    )
    plot_path = ROOT_SCRIPT_PATH / "clean_data_plot.png"
    logger.info(f"Exporting the plot to: {plot_path}")
    figure = ax.get_figure()
    if figure and isinstance(figure, Figure):
        figure.savefig(plot_path)
    logger.success("Plot exported successfully.")


def user_select_file_to_clean() -> Path:
    """Ask user to select files to clean and return the list of selected files."""
    all_txt_files_in_path = list(ROOT_SCRIPT_PATH.glob("*.txt"))
    if not all_txt_files_in_path:
        logger.warning("No .txt files found in the path.")

    logger.info("Select the files you want to clean:")
    paths_with_index = dict(enumerate(all_txt_files_in_path, start=1))
    for i, path in paths_with_index.items():
        logger.info(f"{i}) {path.name}")

    try:
        selected_file_idex = int(input("Enter the file number you want to clean: "))
    except ValueError:
        logger.error("Invalid file number selected. Use only numbers.")
        sys.exit(1)
    selected_file_path = paths_with_index.get(selected_file_idex)
    if not selected_file_path:
        logger.error("Invalid file number selected.")
        sys.exit(1)
    return selected_file_path


def user_select_file_format() -> FileTypes:
    """Ask user to select the file format to export the cleaned data."""
    logger.info("Choose the file format to export the cleaned data:")
    for file_type in FileTypes:
        logger.info(f"-->>> {file_type.value}")
    file_type = input("Enter the file format: ")
    if file_type not in [file_type.value for file_type in FileTypes]:
        logger.error("Invalid file format selected.")
        sys.exit(1)
    return FileTypes(file_type)


def user_select_export_plot() -> bool:
    """Ask user if they want to export a plot."""
    logger.info("Do you want to export a plot?")
    export_plot = input("Enter 'yes' or 'no': ")
    if export_plot not in ["yes", "no"]:
        logger.error("Invalid input. Please enter 'yes' or 'no'.")
        sys.exit(1)
    return export_plot == "yes"


def main() -> None:
    """Run the main function for the script."""
    logger.info("Starting the script for converting raw data to clean data.")
    logger.debug(f"--> Root script path: {ROOT_SCRIPT_PATH}")
    file_to_parse = user_select_file_to_clean()
    logger.success(f"Selected file to clean: {file_to_parse}")
    clean_data_df = parse_raw_data_to_dataframe(file_to_parse)
    file_type = user_select_file_format()
    export_data_to_file(clean_data_df, file_type)
    export_data_to_plot(clean_data_df) if user_select_export_plot() else None
    logger.success("Script finished successfully.")


if __name__ == "__main__":
    main()
