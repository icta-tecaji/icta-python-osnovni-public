import pandas as pd
from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


raw_file_path = get_absolute_file_path("plume_central_web_application.txt")

final_data = pd.read_csv(raw_file_path)["Tested By"].value_counts().to_dict()

print(final_data)
