"""Scraper for web data."""

from __future__ import annotations

import asyncio
import datetime  # noqa: TC003
import json
import time
from pathlib import Path

import aiofiles
import bs4
import httpx
from loguru import logger
from pydantic import BaseModel, Field

BASE_URL = "https://talkpython.fm"
FILE_PATH = Path(__file__).parent / "data.txt"


class BlogMetadata(BaseModel):
    """Model for blog metadata."""

    url: str
    name: str
    episode_number: int = Field(validation_alias="episodeNumber")
    description: str
    date_published: datetime.date = Field(validation_alias="datePublished")


async def fetch_website_data(url: str) -> str | None:
    """Fetch the data from the website."""
    try:
        logger.debug(f"Fetching data from {url}...")
        start_time = time.time()
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)

        if response.status_code != httpx.codes.OK:
            logger.error(f"Failed to fetch data from {url}.")
            return None
    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to fetch data from {url}. Exception: {e}")
        return None
    else:
        logger.debug(f"Fetched data from {url} in {time.time() - start_time:.2f} seconds.")
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


async def save_website_data(data: BlogMetadata) -> None:
    """Save the data to the database."""
    logger.debug(f"Saving data to {FILE_PATH} for episode {data.episode_number}...")
    async with aiofiles.open(FILE_PATH, "a") as file:
        data_dict = data.model_dump()
        values = ",".join(f"{value}" for value in data_dict.values())
        await file.write(values + "\n")


def reset_file() -> None:
    """Reset the file."""
    with FILE_PATH.open("w") as file:
        file.write("")


async def scrape_single_episode(episode_number: int) -> None:
    """Scrape a single episode."""
    url = f"{BASE_URL}/{episode_number}"
    logger.info(f"Fetching data from {url}...")
    data = await fetch_website_data(url)
    parsed_data = parse_website_data(data)
    if not parsed_data:
        logger.warning(f"No data to parse found in response from {url}.")
        return
    await save_website_data(parsed_data)


async def main() -> None:
    """Entrypoint of the application."""
    start_time = time.time()
    reset_file()

    episodes_numbers = range(50, 71)
    await asyncio.gather(*[scrape_single_episode(episode_number) for episode_number in episodes_numbers])
    logger.success(f"Finished in {time.time() - start_time:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
