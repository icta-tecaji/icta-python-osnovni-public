import asyncio
import time
from pathlib import Path

import uvloop
from httpx import AsyncClient

POP20_CC = "CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR".split()

BASE_URL = "https://www.fluentpython.com/data/flags"
DEST_DIR = Path(__file__).parent.joinpath("downloaded")


def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)


async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
    resp = await client.get(url, timeout=7, follow_redirects=True)
    return resp.read()


async def download_one(client: AsyncClient, cc: str) -> str:
    image = await get_flag(client, cc)
    await asyncio.to_thread(save_flag, image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc


async def suprevisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:
        coros = [download_one(client, cc) for cc in sorted(cc_list)]
        res = await asyncio.gather(*coros)
    return len(res)


def download_many(cc_list: list[str]) -> int:
    uvloop.install()
    return asyncio.run(suprevisor(cc_list))


def main(downloader):
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f"\n{count} downloads in {elapsed:.2f}s")


if __name__ == "__main__":
    main(download_many)
