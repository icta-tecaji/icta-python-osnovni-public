"""Download URLs concurrently using threading."""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from loguru import logger

URLS = [
    "https://docs.python.org/3/library/concurrency.html",
    "https://docs.python.org/3/library/concurrent.html",
    "https://docs.python.org/3/library/concurrent.futures.html",
    "https://docs.python.org/3/library/threading.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://docs.python.org/3/library/multiprocessing.shared_memory.html",
    "https://docs.python.org/3/library/subprocess.html",
    "https://docs.python.org/3/library/queue.html",
    "https://docs.python.org/3/library/sched.html",
    "https://docs.python.org/3/library/contextvars.html",
]


def download_url(url: str, timeout: int = 5) -> tuple[str | None, str]:
    """Download a URL."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        logger.debug(f"Downloaded {len(response.content)} bytes from {url}.")
    except Exception as e:  # noqa: BLE001
        logger.error(f"Error downloading {url}: {e}")
        return None, url
    else:
        return response.text, url


def save_file(url: str, data: str, path: Path) -> None:
    """Save data to a file."""
    file_path = path / f"{url.split('/')[-1]}.html"
    with file_path.open("w", encoding="utf-8") as file:
        file.write(data)
    logger.debug(f"Saved {len(data)} bytes to {file_path}.")


def download_docs(urls: list[str], path: Path) -> None:
    """Download URLs concurrently."""
    # create folder if it doesn't exist
    path.mkdir(parents=True, exist_ok=True)
    number_of_threads = len(urls)
    with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        futures = [executor.submit(download_url, url) for url in urls]
        for future in as_completed(futures):
            data, url = future.result()
            if not data:
                logger.warning(f"No data to save for {url}. Skipping...")
                continue
            save_file(url, data, path)
            logger.success(f"Downloaded {url}.")


if __name__ == "__main__":
    start_time = time.time()
    path = Path(__file__).parent / "downloads"
    download_docs(URLS, path)
    logger.info(f"Downloaded all URLs in {time.time() - start_time:.2f} seconds.")
