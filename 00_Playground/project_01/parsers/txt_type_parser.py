"""Txt type parser module."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class NoDataError(Exception):
    """Exception raised when no data is loaded."""


class TxtTypeParser:
    """Class to parse a txt type file."""

    def __init__(self: TxtTypeParser, file_path: Path) -> None:
        """Initialize the TxtTypeParser class."""
        self.file_path = file_path

    def load_data(self: TxtTypeParser) -> pd.DataFrame:
        """Load the data from the txt file."""
        return self.__parse_data()

    def __parse_data(self: TxtTypeParser) -> pd.DataFrame:
        """Parse the data from the txt file."""
        raw_data = pd.read_csv(self.file_path, sep="\t")
        raw_data.columns = [column.strip().lower().replace(" ", "_") for column in raw_data.columns]
        if raw_data.columns[-1].startswith("unnamed"):
            raw_data = raw_data.drop(raw_data.columns[-1], axis=1)
        raw_data["time"] = pd.to_datetime(raw_data["time"], format="%Y-%m-%d %H:%M:%S.%f")
        return raw_data


if __name__ == "__main__":
    txt_type_parser = TxtTypeParser(Path("../data/power-40-0711-16-45.txt"))
    data = txt_type_parser.load_data()
    print(data.head())  # noqa: T201
