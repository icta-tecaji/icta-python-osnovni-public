import asyncio
import time


async def f(delay, what):
    await asyncio.sleep(delay)
    print("function f", what)
    return what


async def g(delay, what):
    await asyncio.sleep(delay)
    print("function g", what)
    return what


async def h(delay, what):
    await asyncio.sleep(delay)
    raise ValueError
    print("function h", what)
    return what


async def main():
    print(f"started at {time.strftime('%X')}")
    # pokažemo še brez return_exceptions=True
    result = await asyncio.gather(
        f(2, "prva"), g(2, "druga"), h(2, "tretja"), return_exceptions=True
    )
    for res in result:
        if isinstance(res, ValueError):
            print("pohandlam error")
    print(f"finished at {time.strftime('%X')}")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
