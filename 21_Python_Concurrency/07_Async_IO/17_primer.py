import asyncio
import aiohttp


class AsyncSession:
    def __init__(self, url) -> None:
        self.url = url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        response = await self.session.get(self.url)
        return response

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.session.close()


async def check(url):
    async with AsyncSession(url) as response:
        html = await response.text()
        print(f"Status: {response.status}")
        print(f"Data: {html[:20].strip()}")


async def main():
    await asyncio.gather(
        check("https://docs.python.org/"), check("https://github.com/")
    )


if __name__ == "__main__":
    asyncio.run(main())
