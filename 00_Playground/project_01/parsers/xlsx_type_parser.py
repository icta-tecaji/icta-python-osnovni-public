"""Xlsx type parser module."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class NoDataError(Exception):
    """Exception raised when no data is loaded."""


class XlsxTypeParser:
    """Class to parse a xlsx type file."""

    def __init__(self: XlsxTypeParser, file_path: Path) -> None:
        """Initialize the XlsxTypeParser class."""
        self.file_path = file_path

    def load_data(self: XlsxTypeParser) -> pd.DataFrame:
        """Load the data from the xlsx file."""
        return self.__parse_data()

    def __parse_data(self: XlsxTypeParser) -> pd.DataFrame:
        """Parse the data from the xlsx file."""
        raw_data = pd.read_excel(self.file_path, engine="openpyxl", sheet_name="Data")
        raw_data.columns = [column.strip().lower().replace(" ", "_") for column in raw_data.columns]
        raw_data["time"] = pd.to_datetime(raw_data["time"], format="%d. %m. %Y %H:%M:%S")
        return raw_data


if __name__ == "__main__":
    xlsx_type_parser = XlsxTypeParser(Path("../data/02.01.07_873740_log.xlsx"))
    data = xlsx_type_parser.load_data()
    print(data.head())  # noqa: T201
