import time
import requests
from typing import List
import multiprocessing

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url: str):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"[{name}] Read {len(response.content)} from {url}.")


def download_all_sites(sites_url: List):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites_url)


if __name__ == "__main__":
    sites = ["https://example.com/", "https://www.python.org/"] * 30
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds.")
