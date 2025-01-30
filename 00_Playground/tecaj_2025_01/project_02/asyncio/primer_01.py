import asyncio
import time

from loguru import logger


async def fetch_network_data(number: int) -> int:
    """Simulate fetching data from a network."""
    print(f"Start fetching data from network: {number}...")
    await asyncio.sleep(1)
    if number == 3:
        raise ValueError("Something went wrong!")
    print(f"Fetching data from network: {number}")
    return number * number


async def get_disk_data(number: int) -> int:
    """Simulate fetching data from disk."""
    await asyncio.sleep(2)
    print(f"Fetching data from disk: {number}")
    return number * number * number


async def main() -> None:
    """Main entry point of the app."""
    start_time = time.time()
    results = await asyncio.gather(
        fetch_network_data(1),
        fetch_network_data(2),
        fetch_network_data(3),
        fetch_network_data(4),
        return_exceptions=True,
    )
    results_new = []
    for result in results:
        if isinstance(result, Exception):
            logger.warning(f"An error occurred: {result}")
            results_new.append(0)
        else:
            results_new.append(result)

    result1, result2, result3, result4 = results_new
    print(f"Results: {result1}, {result2}, {result3}, {result4}")

    results = await asyncio.gather(
        get_disk_data(result1),
        get_disk_data(result2),
        get_disk_data(result3),
        get_disk_data(result4),
    )
    result5, result6, result7, result8 = results
    print(f"Results: {result5}, {result6}, {result7}, {result8}")
    print(f"Execution time: {time.time() - start_time:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
