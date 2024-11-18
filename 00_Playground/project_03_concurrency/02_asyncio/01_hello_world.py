import asyncio
import time


async def fetch_network_data(number):
    await asyncio.sleep(1)
    print(f"Fetching network data for {number}")
    if number == 3:
        raise ValueError("Something went wrong")
    return number * number


async def get_disk_data(network_number):
    await asyncio.sleep(2)
    if isinstance(network_number, Exception):
        print(f"Error occurred: {network_number}. Cannot fetch disk data")
        return None
    print(f"Fetching disk data for {network_number}")
    return network_number * network_number * network_number


async def main():
    start_time = time.time()
    results = await asyncio.gather(
        fetch_network_data(1),
        fetch_network_data(2),
        fetch_network_data(3),
        fetch_network_data(4),
        return_exceptions=True,
    )
    print(results)
    disk_results = await asyncio.gather(
        get_disk_data(results[0]),
        get_disk_data(results[1]),
        get_disk_data(results[2]),
        get_disk_data(results[3]),
    )
    print(f"Time taken: {time.time() - start_time}")
    print(disk_results)


if __name__ == "__main__":
    asyncio.run(main())
