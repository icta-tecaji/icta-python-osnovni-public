import queue
import time
import asyncio


async def task(name, work_queue: queue.Queue):
    while not work_queue.empty():
        count = await work_queue.get()
        print(f"Task {name} running!")
        await asyncio.sleep(count)


async def main():
    working_queue = asyncio.Queue()
    for work in [15, 10, 5, 2]:
        await working_queue.put(work)

    tasks = [
        asyncio.create_task(task("one", working_queue)),
        asyncio.create_task(task("two", working_queue)),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Duration: {end - start}")
