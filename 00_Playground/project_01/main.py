"""Main module of the project."""
from __future__ import annotations

import glob
import sys
from typing import TYPE_CHECKING, Any

from exporters.dataframe_exporter import DataFrameExporter
from helpers.file_manipulation import FileInfo
from helpers.file_manipulation import FileManipulationHelpers as fmh
from parsers.log_type_parser import LogTypeParser
from parsers.txt_type_parser import TxtTypeParser
from parsers.xlsx_type_parser import XlsxTypeParser

if TYPE_CHECKING:
    import pandas as pd


def get_file_path_from_user() -> list[FileInfo]:
    """Return the file path from the user."""
    folder_name = input("Enter the name of the folder: ")
    full_folder_path = fmh.get_absolute_path(__file__, folder_name)
    if not fmh.validate_if_path_is_existing_folder(full_folder_path):
        print("The data folder does not exist. Exiting...")
        sys.exit(1)

    parsable_files = fmh.get_all_files_from_folder(full_folder_path)
    parsable_files_dict = {file.file_id: file for file in parsable_files}
    fmh.print_folder_info(parsable_files)
    file_select_mode = input("Enter select mode [1) id, 2) multiple, 3) glob pattern]: ")
    file_ids = []

    if file_select_mode == "1":
        file_id = input("Enter the file ID: ")
        try:
            file_ids = [int(file_id, 10)]
        except ValueError:
            print("The file ID must be an integer. Exiting...")
            sys.exit(1)
    elif file_select_mode == "2":
        file_ids = input("Enter the file IDs separated by a comma: ")
        file_ids = file_ids.split(",")
        try:
            file_ids = [int(file_id, 10) for file_id in file_ids]
        except ValueError:
            print("The file IDs must be integers. Exiting...")
            sys.exit(1)
    elif file_select_mode == "3":
        glob_pattern = input("Enter the glob pattern: ")
        file_matches_ids = glob.glob(f"{full_folder_path}/{glob_pattern}")
        for file in parsable_files:
            if str(file.path) in file_matches_ids:
                file_ids.append(file.file_id)

    for file_id in file_ids:
        if file_id not in parsable_files_dict:
            print("The file ID does not exist. Exiting...")
            sys.exit(1)

    print(f"File to parse: {[file.name for file in parsable_files if file.file_id in file_ids]}")
    return [parsable_files_dict[file_id] for file_id in file_ids]


def load_and_parse_file(file: FileInfo) -> tuple[pd.DataFrame, Any]:
    """Load and parse the file."""
    if file.extension == "log":
        parser = LogTypeParser(file.path)
        return parser.load_data(), parser.load_metadata()

    if file.extension == "txt":
        parser = TxtTypeParser(file.path)
        return parser.load_data(), None

    if file.extension == "xlsx":
        parser = XlsxTypeParser(file.path)
        return parser.load_data(), None

    print("The file extension is not supported. Exiting...")
    sys.exit(1)


def run_export_operation(
    data: pd.DataFrame,
    metadata: Any,
    operation: int,
    file_to_parse: FileInfo,
    output_folder_name: str,
) -> None:
    """Run the export operation."""
    output_folder = fmh.get_absolute_path(__file__, output_folder_name)
    fmh.create_all_folders_in_path(output_folder)
    exporter = DataFrameExporter(data, metadata.__dict__) if metadata is not None else DataFrameExporter(data)

    if operation == 1:
        exporter.to_csv(output_folder / f"{file_to_parse.name}.csv")
    elif operation == 2:
        exporter.to_json(output_folder / f"{file_to_parse.name}.json")
    elif operation == 3:
        exporter.to_excel(output_folder / f"{file_to_parse.name}.xlsx")
    elif operation == 4:
        exporter.to_csv(output_folder / f"{file_to_parse.name}.csv")
        exporter.to_json(output_folder / f"{file_to_parse.name}.json")
        exporter.to_excel(output_folder / f"{file_to_parse.name}.xlsx")
    else:
        print("Invalid operation. Exiting...")
        sys.exit(1)

    print(f"Done {file_to_parse.name}.")


def main() -> None:
    """Entry point of the program."""
    # 1. Get file path from user
    file_to_parse = get_file_path_from_user()

    # 2. Select operation to perform on the data
    print("Select operation to perform on the data:")
    print("1. Export to CSV")
    print("2. Export to JSON")
    print("3. Export to Excel")
    print("4. Export to all formats")
    print("5. Exit")
    operation = input("Enter the operation number: ")

    if operation in ("1", "2", "3", "4"):
        output_folder_name = input("Enter the name of the output folder: ")

    # 3. Parse and load the file
    for file in file_to_parse:
        print(f"Processing file: {file.name}")
        data, metadata = load_and_parse_file(file)
        if operation in ("1", "2", "3", "4"):
            run_export_operation(data, metadata, int(operation, 10), file, output_folder_name)  # type: ignore
        elif operation == "5":
            sys.exit(0)
        else:
            print("Invalid operation. Exiting...")
            sys.exit(1)

    # Izdelava grafov - statčni graf x/y

    # Zagon dinamične analize
    # TODO: ponedeljek

    # Web aplikacija za manipuliranje in analizo podatkov
    # TODO: četrtek


if __name__ == "__main__":
    main()
