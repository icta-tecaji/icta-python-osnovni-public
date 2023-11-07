import asyncio
import socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4
ROOT_DOMAIN = "dev"


async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def main():
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f"{name}.{ROOT_DOMAIN}" for name in names)
    coros = [probe(domain) for domain in domains]
    for coro in asyncio.as_completed(coros):
        domain, found = await coro
        mark = "+" if found else " "
        print(f"{mark} {domain}")


if __name__ == "__main__":
    asyncio.run(main())
