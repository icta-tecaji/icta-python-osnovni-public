import asyncio
import socket
from typing import NamedTuple
import sys
from keyword import kwlist

MAX_KEYWORD_LEN = 4


class Result(NamedTuple):
    domain: str
    status: bool


async def probe(domain: str, loop=None) -> tuple[str, bool]:
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains):
    loop = asyncio.get_running_loop()
    cooros = [probe(domain, loop) for domain in domains]

    for coro in asyncio.as_completed(cooros):
        result = await coro
        yield result


async def main(tld: str):
    tld = tld.strip(".")
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f"{name}.{tld}" for name in names)
    async for domain, found in multi_probe(domains):
        print(f"{domain} - {found}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        asyncio.run(main(sys.argv[1]))
    else:
        print("Provide a TLD like com, dev")
