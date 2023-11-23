"""File manipulation helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileInfo:
    """Class to store file information."""

    file_id: int
    name: str
    path: Path
    size: int
    extension: str


class FileManipulationHelpers:
    """Class to provide file manipulation helpers."""

    @staticmethod
    def get_absolute_path(file_path: str, relative_path: str) -> Path:
        """Return the absolute path of a file or directory."""
        return Path(file_path).parent / relative_path

    @staticmethod
    def validate_if_path_is_existing_folder(path: Path) -> bool:
        """Validate if the path is an existing folder."""
        return path.is_dir()

    @staticmethod
    def get_all_files_from_folder(path: Path) -> list[FileInfo]:
        """Return all files from a folder."""
        results = []
        with os.scandir(path) as dir_contents:
            for file_id, entry in enumerate(dir_contents):
                if entry.is_file():
                    file_info = FileInfo(
                        file_id=file_id,
                        name=entry.name,
                        path=Path(entry.path),
                        size=entry.stat().st_size,
                        extension=entry.name.split(".")[-1],
                    )
                    results.append(file_info)
        return results

    @staticmethod
    def print_folder_info(files: list[FileInfo]) -> None:
        """Print folder information."""
        print(
            "  FILE ID  |          FILE NAME          |     FILE SIZE   |  FILE EXTENSION",
        )
        for file in files:
            FileManipulationHelpers.print_file_info(file)

    @staticmethod
    def print_file_info(file_info: FileInfo) -> None:
        """Print file information."""
        print(
            f"  {file_info.file_id: <7}  |  {file_info.name[:22]+'...': <25}  |  {round(file_info.size/1024/1024, 4): <10}  MB |  {file_info.extension: <10}",
        )

    @staticmethod
    def create_all_folders_in_path(path: Path) -> None:
        """Create all folders in the path."""
        path.mkdir(parents=True, exist_ok=True)
