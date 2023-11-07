import asyncio
import os
import time
from pathlib import Path

import aiofiles
import aiohttp


def get_absolute_file_path(relative_path: str) -> str:
    return str(Path(__file__).parent.joinpath(relative_path))


async def write_genre(file_name):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the
    name of the given file
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://binaryjazz.us/wp-json/genrenator/v1/genre/"
        ) as response:
            genre = await response.json()

    async with aiofiles.open(file_name, "w") as new_file:
        print(f"Writing '{genre}' to '{file_name}'...")
        await new_file.write(genre)


async def main():
    path = get_absolute_file_path("sync")
    os.makedirs(path, exist_ok=True)

    print("Starting...")
    start = time.perf_counter()

    tasks = [write_genre(f"{path}/new_file{i}.txt") for i in range(10)]
    await asyncio.gather(*tasks)

    end = time.perf_counter()
    print(f"Time to complete synchronous read/writes: {round(end - start, 2)} seconds")


if __name__ == "__main__":
    asyncio.run(main())
