import time
import requests
from typing import List


def download_site(url: str, session: requests.Session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}.")


def download_all_sites(sites_url: List):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


if __name__ == "__main__":
    sites = ["https://example.com/", "https://www.python.org/"] * 30
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds.")
