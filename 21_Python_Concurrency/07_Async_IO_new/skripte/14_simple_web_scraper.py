import asyncio
import aiohttp
import bs4
import time
from colorama import Fore


async def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f"https://talkpython.fm/{episode_number}"
    # resp = await requests.get(url) -> ta del najdlje traja zato ga damo na async, probelm da knjižnica request ni async
    async with aiohttp.ClientSession() as session:  # pridovinaje seje je asinhrono, zato moremo dodat še async
        async with session.get(url) as resp:  # asinhorn začetek http zahtevka
            resp.raise_for_status()
            html = await resp.text()  # čakanje na podatke iz srverja
            return (html, episode_number)


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, "html.parser")
    header = soup.select_one("h1")
    if not header:
        return "MISSING"

    return header.text.strip()


async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    tasks = []
    for n in range(185, 200):
        tasks.append(asyncio.create_task(get_html(n)))

    results = await asyncio.gather(*tasks)

    for html, episode_number in results:
        title = get_title(
            html, episode_number
        )  # to je procesiranje v pomnilniku zato ni problematično, async ne pohitri, edina rešitev mulitprocesing
        print(Fore.WHITE + f"Title found: {title}", flush=True)


def main():
    start = time.perf_counter()
    asyncio.run(get_title_range())
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
    print("Done.")


if __name__ == "__main__":
    main()
