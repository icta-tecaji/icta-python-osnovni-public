"""Scraper for web data."""

from __future__ import annotations

import datetime  # noqa: TC003
import json
import time
from pathlib import Path

import bs4
import httpx
from loguru import logger
from pydantic import BaseModel, Field

FILE_PATH = Path(__file__).parent / "data.txt"


class BlogMetadata(BaseModel):
    """Model for blog metadata."""

    url: str
    name: str
    episode_number: int = Field(validation_alias="episodeNumber")
    description: str
    date_published: datetime.date = Field(validation_alias="datePublished")


def fetch_website_data(url: str) -> str | None:
    """Fetch the data from the website."""
    logger.debug(f"Fetching data from {url}...")
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)

    if response.status_code != httpx.codes.OK:
        logger.error(f"Failed to fetch data from {url}.")
        return None
    return response.text


def parse_website_data(data: str | None) -> BlogMetadata | None:
    """Parse the data from the website."""
    if not data:
        return None
    soup = bs4.BeautifulSoup(data, "html.parser")
    script_tag = soup.find("script", {"type": "application/ld+json"})
    if not script_tag:
        logger.warning("No script tag found.")
        return None

    script_text = script_tag.text
    json_data = json.loads(script_text)
    raw_metadata = json_data["@graph"][0]
    parsed_data = BlogMetadata.model_validate(raw_metadata)
    logger.debug(f"Parsing data from the website for episode {parsed_data.episode_number}...")
    return parsed_data


def save_website_data(data: BlogMetadata) -> None:
    """Save the data to the database."""
    logger.debug(f"Saving data to {FILE_PATH} for episode {data.episode_number}...")
    with FILE_PATH.open("a") as file:
        data_dict = data.model_dump()
        values = ",".join(f"{value}" for value in data_dict.values())
        file.write(values + "\n")


def reset_file() -> None:
    """Reset the file."""
    with FILE_PATH.open("w") as file:
        file.write("")


def main() -> None:
    """Entrypoint of the application."""
    start_time = time.time()
    reset_file()
    base_url = "https://talkpython.fm"
    episodes_numbers = [85, 86, 87, 88, 89, 90, 91]

    for episode_number in episodes_numbers:
        url = f"{base_url}/{episode_number}"
        logger.info(f"Fetching data from {url}...")
        data = fetch_website_data(url)
        parsed_data = parse_website_data(data)
        if not parsed_data:
            logger.warning(f"No data to parse found in response from {url}.")
            continue
        save_website_data(parsed_data)

    logger.success(f"Finished in {time.time() - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()
