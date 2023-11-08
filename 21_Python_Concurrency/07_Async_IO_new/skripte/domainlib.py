import asyncio
import socket
import sys
from collections.abc import AsyncIterator, Iterable
from keyword import kwlist
from typing import NamedTuple


class Result(NamedTuple):
    domain: str
    found: bool


async def probe(domain: str, loop: asyncio.AbstractEventLoop = None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro
        yield result


async def main(tld: str) -> None:
    tld = tld.strip(".")
    names = (kw for kw in kwlist if len(kw) <= 4)
    domains = (f"{name}.{tld}".lower() for name in names)
    print("FOUND\t\tNOT FOUND")
    print("=====\t\t=========")
    async for domain, found in multi_probe(domains):
        indent = "" if found else "\t\t"
        print(f"{indent}{domain}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        asyncio.run(main(sys.argv[1]))  # <6>
    else:
        print("Please provide a TLD.", f"Example: {sys.argv[0]} COM.BR")
