"""Log type parser module."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path

import pandas as pd


@dataclass
class LogFileMetadata:
    """Class to hold the metadata of a log file."""

    pu_version: str
    pu_hash: str
    pu_version_classb: str
    pu_hash_classb: str
    mu_version: str
    mu_hash: str
    mu_version_classb: str
    mu_hash_classb: str
    ui_version: str
    ui_hash: str
    ui_version_classb: str
    ui_hash_classb: str
    wifi_version: str
    wifi_hash: str
    wifi_version_classb: str
    wifi_hash_classb: str
    hw_pmcu_version: str
    hw_ui_version: str
    hw_varcode: str


class NoMetadataError(Exception):
    """Exception raised when no metadata is loaded."""


class NoDataError(Exception):
    """Exception raised when no data is loaded."""


class LogTypeParser:
    """Class to parse a log type file."""

    NUMBER_OF_METADATA_LINES = 2

    def __init__(self: LogTypeParser, file_path: Path) -> None:
        """Initialize the LogTypeParser class."""
        self.file_path = file_path
        self.raw_metadata: None | list[str] = None
        self.raw_data: None | list[str] = None

    def load_metadata(self: LogTypeParser) -> LogFileMetadata:
        """Load the metadata from the log file."""
        if self.raw_metadata is None:
            self.__parse()
        return self.__parse_metadata()

    def load_data(self: LogTypeParser) -> pd.DataFrame:
        """Load the data from the log file."""
        if self.raw_data is None:
            self.__parse()
        return self.__parse_data()

    def __parse(self: LogTypeParser) -> None:
        self.raw_metadata, self.raw_data = self.__load_raw_data()

    def __parse_metadata(self: LogTypeParser) -> LogFileMetadata:
        if not self.raw_metadata:
            raise NoMetadataError(self.raw_metadata)

        field_names = self.raw_metadata[0].split("\t")
        field_names = [field_name.strip().lower().replace(" ", "_") for field_name in field_names]

        field_values = self.raw_metadata[1].split("\t")
        field_values = [field_value.strip().replace("'", "") for field_value in field_values]

        return LogFileMetadata(**dict(zip(field_names, field_values)))

    def __parse_data(self: LogTypeParser) -> pd.DataFrame:
        if not self.raw_data:
            raise NoDataError(self.raw_data)

        data = pd.read_csv(StringIO("".join(self.raw_data)), sep="\t", na_values=["/"])
        data.columns = [column.strip().lower().replace(" ", "_") for column in data.columns]
        data = data.drop(columns=["unnamed:_76"])
        data["time"] = pd.to_datetime(data["time"].str.replace("'", ""), format="%Y-%m-%d %H:%M:%S,%f")
        return data

    def __load_raw_data(self: LogTypeParser) -> tuple[list[str], list[str]]:
        with self.file_path.open() as f:
            raw_data = f.readlines()
        return (raw_data[: self.NUMBER_OF_METADATA_LINES], raw_data[self.NUMBER_OF_METADATA_LINES :])


if __name__ == "__main__":
    log_type_parser = LogTypeParser(Path("../data/OutputLog_COM51_20231114-160929.log"))
    metadata = log_type_parser.load_metadata()
    data = log_type_parser.load_data()
    print(metadata)  # noqa: T201
    print(data)  # noqa: T201
