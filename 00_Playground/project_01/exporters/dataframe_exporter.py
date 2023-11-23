"""Class to export data frames to different formats."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from pathlib import Path


class ExportParentFolderDoesNotExistError(Exception):
    """Exception raised when the parent folder does not exist."""

    def __init__(self: ExportParentFolderDoesNotExistError, path: Path) -> None:
        """Initialize the ExportParentFolderDoesNotExistError class."""
        super().__init__(f"The parent folder {path.parent} does not exist.")


class DataFrameExporter:
    """Class to export data frames to different formats."""

    def __init__(self: DataFrameExporter, data: pd.DataFrame, metadata: dict | None = None) -> None:
        """Initialize the DataFrameExporter class."""
        self.data = data
        self.metadata = metadata

    def to_csv(self: DataFrameExporter, path: Path) -> None:
        """Export the data frame to a CSV file."""
        self.__raise_if_parent_folder_exists(path)
        self.data.to_csv(path, index=False)

        if self.metadata is not None:
            final_data = {"metadata": self.metadata}
            # add _metadata to the file name
            path = path.parent / f"{path.stem}_metadata.json"
            with path.open("w") as file:
                json.dump(final_data, file, indent=4)

    def to_excel(self: DataFrameExporter, path: Path) -> None:
        """Export the data frame to an Excel file."""
        self.__raise_if_parent_folder_exists(path)
        with pd.ExcelWriter(path, engine="openpyxl", mode="w") as writer:
            # add data to data sheet
            self.data.to_excel(writer, sheet_name="data", index=False)
            if self.metadata is not None:
                df_metadata = pd.DataFrame(self.metadata, index=[0])
                df_metadata.to_excel(writer, sheet_name="metadata", index=False)

    def to_json(self: DataFrameExporter, path: Path) -> None:
        """Export the data frame to a JSON file."""
        self.__raise_if_parent_folder_exists(path)
        self.data.to_json(path, orient="records", date_format="iso")

        if self.metadata is not None:
            final_data = {"metadata": self.metadata}
            # add _metadata to the file name
            path = path.parent / f"{path.stem}_metadata{path.suffix}"
            with path.open("w") as file:
                json.dump(final_data, file, indent=4)

    def __raise_if_parent_folder_exists(self: DataFrameExporter, path: Path) -> None:
        """Check if the path exists."""
        if not path.parent.exists():
            raise ExportParentFolderDoesNotExistError(path)
