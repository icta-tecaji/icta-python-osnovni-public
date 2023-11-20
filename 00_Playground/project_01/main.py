from __future__ import annotations

import os
import sys
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


def get_absolute_path(relative_path: str) -> Path:
    """Return the absolute path of a file or directory."""
    return Path(__file__).parent / relative_path


def validate_if_path_is_existing_folder(path: Path) -> bool:
    """Validate if the path is an existing folder."""
    return path.is_dir()


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


def print_file_info(file_info: FileInfo) -> None:
    """Print file information."""
    print(
        f"  {file_info.file_id: <7}  |  {file_info.name[:22]+'...': <25}  |  {round(file_info.size/1024/1024, 4): <10}  MB |  {file_info.extension: <10}",
    )


def main() -> None:
    """Entry point of the program."""
    # Get folder name from user for the directory with the files
    folder_name = input("Enter the name of the folder: ")
    full_folder_path = get_absolute_path(folder_name)
    print(f"Folder path: {full_folder_path}")
    if validate_if_path_is_existing_folder(full_folder_path):
        parsable_files = get_all_files_from_folder(full_folder_path)
        print(
            "  FILE ID  |          FILE NAME          |     FILE SIZE   |  FILE EXTENSION",
        )
        for file in parsable_files:
            print_file_info(file)
    else:
        print("The folder does not exist. Exiting...")
        sys.exit(1)

    # Get file id from user for the file to parse
    file_id = int(input("Enter the file ID: "))
    file_to_parse = parsable_files[file_id]
    print(f"File to parse: {file_to_parse.name}")


main()
