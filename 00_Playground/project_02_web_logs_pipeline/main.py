"""Main module for the web logs parsing pipeline."""

from __future__ import annotations

import datetime
import json
import sys
import time
from collections import Counter
from pathlib import Path

import httpx
import pandas as pd
from loguru import logger

MAIN_DATA_FOLDER = Path(__file__).parent / "data"
MAIN_LOG_DATA_SOURCE_LINK = (
    "https://raw.githubusercontent.com/elastic/examples/refs/heads/master/Common%20Data%20Formats/nginx_json_logs/nginx_json_logs"
)

# Configure logger
logger.remove()
logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
logger.add(sys.stderr, format=logger_format, level="DEBUG")


def read_and_parse_raw_logs_data_pd(file_path: Path) -> pd.DataFrame:
    """Read and parse raw logs data from the provided file path."""
    start_time = time.time()
    raw_data = pd.read_json(file_path, lines=True)
    # Rename time to timestamp and convert to datetime
    raw_data.rename(columns={"time": "timestamp"}, inplace=True)  # noqa: PD002
    raw_data["timestamp"] = pd.to_datetime(raw_data["timestamp"], format="%d/%b/%Y:%H:%M:%S %z")
    # Rename remote_ip to client_ip
    raw_data.rename(columns={"remote_ip": "client_ip"}, inplace=True)  # noqa: PD002
    # Split request into method, url, and protocol and keep only the url
    raw_data["url"] = raw_data["request"].str.split(" ").str[1]
    # Drop the original request column and unused columns
    raw_data = raw_data.drop(columns=["remote_user", "referrer", "request"])
    # Rename response to response_code and convert to integer
    raw_data.rename(columns={"response": "response_code"}, inplace=True)  # noqa: PD002
    raw_data["response_code"] = pd.to_numeric(raw_data["response_code"], downcast="integer")
    # Rename bytes to response_size_bytes and convert to integer
    raw_data.rename(columns={"bytes": "response_size_bytes"}, inplace=True)  # noqa: PD002
    raw_data["response_size_bytes"] = pd.to_numeric(raw_data["response_size_bytes"], downcast="integer")
    # Rename agent to user_agent
    raw_data.rename(columns={"agent": "user_agent"}, inplace=True)  # noqa: PD002
    logger.info(f"Reading and parsing raw logs took {time.time() - start_time:.2f} seconds.")
    print(raw_data.head())
    return raw_data


def read_and_parse_raw_logs_data(file_path: Path) -> list[dict]:
    """Read and parse raw logs data from the provided file path."""
    start_time = time.time()
    final_data = []
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            new_line = {}
            line_data = json.loads(line)
            new_line["timestamp"] = datetime.datetime.strptime(line_data["time"], "%d/%b/%Y:%H:%M:%S %z")
            new_line["client_ip"] = line_data["remote_ip"]
            new_line["url"] = line_data["request"].split(" ")[1]
            new_line["response_code"] = int(line_data["response"])
            new_line["response_size_bytes"] = int(line_data["bytes"])
            new_line["user_agent"] = line_data["agent"]
            final_data.append(new_line)
    logger.info(f"Reading and parsing raw logs took {time.time() - start_time:.2f} seconds.")
    return final_data


def print_basic_statistics(parsed_data: list[dict]) -> None:
    """Print basic statistics about the parsed data."""
    start_time = time.time()
    total_requests = len(parsed_data)
    unique_client_ips = len({log["client_ip"] for log in parsed_data})
    unique_urls = len({log["url"] for log in parsed_data})
    unique_user_agents = len({log["user_agent"] for log in parsed_data})
    total_response_size = sum(log["response_size_bytes"] for log in parsed_data)
    # Count number of requests per day and find the day with the most requests
    requests_per_day = Counter(log["timestamp"].date() for log in parsed_data)
    day_with_most_requests, most_requests = requests_per_day.most_common(1)[0]
    # Percentage of successful requests (2xx status codes)
    successful_requests = sum(1 for log in parsed_data if 200 <= log["response_code"] < 300)
    logger.info("**************************************")
    logger.info("Basic statistics:")
    logger.info(f"  - Total requests: {total_requests}")
    logger.info(f"  - Unique client IPs: {unique_client_ips}")
    logger.info(f"  - Unique URLs: {unique_urls}")
    logger.info(f"  - Total response size: {total_response_size / 1024 / 1024 / 1024:.2f} GB")
    logger.info(f"  - Unique user agents: {unique_user_agents}")
    logger.info(f"  - Day with most requests: {day_with_most_requests} with {most_requests} requests")
    logger.info(f"  - Requests per day: {requests_per_day}")
    logger.info(f"  - Percentage of successful requests: {successful_requests / total_requests:.2%}")
    logger.info("**************************************")
    logger.info(f"Printing basic statistics took {time.time() - start_time:.2f} seconds.")


def print_basic_statistics_pd(parsed_data: pd.DataFrame) -> None:
    """Print basic statistics about the parsed data."""
    start_time = time.time()
    total_requests = len(parsed_data)
    unique_client_ips = parsed_data["client_ip"].nunique()
    unique_urls = parsed_data["url"].nunique()
    unique_user_agents = parsed_data["user_agent"].nunique()
    total_response_size = parsed_data["response_size_bytes"].sum()
    # Count number of requests per day and find the day with the most requests
    requests_per_day = parsed_data["timestamp"].dt.date.value_counts()
    day_with_most_requests, most_requests = requests_per_day.idxmax(), requests_per_day.max()
    # Percentage of successful requests (2xx status codes)
    successful_requests = parsed_data["response_code"].between(200, 299).sum()
    logger.info("**************************************")
    logger.info("Basic statistics:")
    logger.info(f"  - Total requests: {total_requests}")
    logger.info(f"  - Unique client IPs: {unique_client_ips}")
    logger.info(f"  - Unique URLs: {unique_urls}")
    logger.info(f"  - Total response size: {total_response_size / 1024 / 1024 / 1024:.2f} GB")
    logger.info(f"  - Unique user agents: {unique_user_agents}")
    logger.info(f"  - Day with most requests: {day_with_most_requests} with {most_requests} requests")
    logger.info(f"  - Requests per day: {requests_per_day}")
    logger.info(f"  - Percentage of successful requests: {successful_requests / total_requests:.2%}")
    logger.info("**************************************")
    logger.info(f"Printing basic statistics took {time.time() - start_time:.2f} seconds.")


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
    # Python native data structures
    parsed_data = read_and_parse_raw_logs_data(main_logs_file_path)
    print_basic_statistics(parsed_data)
    # Pandas DataFrame
    parsed_data_pd = read_and_parse_raw_logs_data_pd(main_logs_file_path)
    print_basic_statistics_pd(parsed_data_pd)

# imamo link z logi
# prenesemo loge v lokalno datoteko
# preberemo loge
# preparsamo loge
# podatke obogatimo (AI dodamo?)
# podatke shranimo v bazo
# nardimo analitiko nad podatki
# prikaz grafikonov in dashbaorda
