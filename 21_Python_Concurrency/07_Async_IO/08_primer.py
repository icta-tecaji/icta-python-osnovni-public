import asyncio
import time


async def say_after(delay, what):
    print("Started")
    await asyncio.sleep(delay)
    print(what)
    return 4


async def main():
    # task1 = asyncio.create_task(say_after(1, "hello"))
    # task2 = asyncio.create_task(say_after(2, "hello"))
    # task3 = asyncio.create_task(say_after(3, "hello"))
    task4 = asyncio.create_task(say_after(4, "hello"))

    print(f"started at {time.strftime('%X')}")
    # await task1
    # await task2
    # await task3

    await task4
    data = await asyncio.gather(
        say_after(1, "hello"), say_after(2, "hello"), say_after(3, "hello")
    )
    print(data)

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
