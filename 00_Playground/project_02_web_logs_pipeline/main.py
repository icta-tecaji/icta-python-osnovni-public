"""Main module for the web logs parsing pipeline."""

import datetime
import sys
from pathlib import Path

import httpx
from loguru import logger

MAIN_DATA_FOLDER = Path(__file__).parent / "data"
MAIN_LOG_DATA_SOURCE_LINK = (
    "https://raw.githubusercontent.com/elastic/examples/refs/heads/master/Common%20Data%20Formats/nginx_json_logs/nginx_json_logs"
)

# Configure logger
logger.remove()
logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
logger.add(sys.stderr, format=logger_format, level="DEBUG")


def download_raw_logs_data(link: str, local_file_path: Path) -> None:
    """Download raw logs data from the provided link."""
    # Skip downloading if the file already exists
    if local_file_path.exists():
        logger.warning(f"File {local_file_path.name} already exists. Skipping download.")
        return

    logger.info(f"Downloading raw logs data from {link} to {local_file_path.name}")
    with httpx.Client() as client:
        response = client.get(link)
        all_raw_data = response.text
        logger.debug(f"Downloaded {len(all_raw_data)} characters of raw data.")
        with local_file_path.open("w", encoding="utf-8") as file:
            file.write(all_raw_data)


if __name__ == "__main__":
    logger.info("Starting web logs pipeline.")
    # Create main data folder if it does not exist
    MAIN_DATA_FOLDER.mkdir(exist_ok=True)
    current_date = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")
    main_logs_file_path = MAIN_DATA_FOLDER / f"web_logs_{current_date}.json"
    download_raw_logs_data(MAIN_LOG_DATA_SOURCE_LINK, main_logs_file_path)

# imamo link z logi
# prenesemo loge v lokalno datoteko
# preberemo loge
# preparsamo loge
# podatke obogatimo (AI dodamo?)
# podatke shranimo v bazo
# nardimo analitiko nad podatki
# prikaz grafikonov in dashbaorda
