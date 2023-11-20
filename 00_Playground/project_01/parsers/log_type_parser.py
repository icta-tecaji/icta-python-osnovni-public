from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class LogFileMetadata:
    pu_version: str
    pu_hash: str
    pu_version_class_b: str
    pu_hash_class_b: str
    mu_version: str
    mu_hash: str
    mu_version_class_b: str
    mu_hash_class_b: str
    ui_version: str
    ui_hash: str
    ui_version_class_b: str
    ui_hash_class_b: str
    wifi_version: str
    wifi_hash: str
    wifi_version_class_b: str
    wifi_hash_class_b: str
    hw_pmcu_version: str
    hw_ui_version: str
    hw_var_code: str


class LogTypeParser:
    """Class to parse a log type file."""

    NUMBER_OF_METADATA_LINES = 2

    def __init__(self: LogTypeParser, file_path: Path) -> None:
        """Initialize the LogTypeParser class."""
        self.file_path = file_path

    def parse(self: LogTypeParser) -> None:
        raw_metadata, raw_data = self.__load_raw_data()

    def load_metadata(self: LogTypeParser) -> LogFileMetadata:
        pass

    def load_data(self: LogTypeParser) -> pd.DataFrame:
        pass

    def __parse_metadata(self: LogTypeParser) -> LogFileMetadata:
        pass

    def __parse_data(self: LogTypeParser) -> pd.DataFrame:
        pass

    def __load_raw_data(self: LogTypeParser) -> tuple[list[str], list[str]]:
        with self.file_path.open() as f:
            raw_data = f.readlines()
        return (raw_data[: self.NUMBER_OF_METADATA_LINES], raw_data[self.NUMBER_OF_METADATA_LINES :])
