import asyncio
import time
from typing import List

import aiohttp


async def download_site(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        print(f"Read {response.content_length} from {url}.")


async def download_all_sites(sites_url: List):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites_url:
            task = asyncio.create_task(download_site(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = ["https://example.com/", "https://www.python.org/"] * 30
    start_time = time.time()
    asyncio.run(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds.")
