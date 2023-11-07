import time
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor
import threading

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url: str):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}.")


def download_all_sites(sites_url: List):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites_url)


if __name__ == "__main__":
    sites = ["https://example.com/", "https://www.python.org/"] * 30
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds.")
