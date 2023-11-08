import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from pathlib import Path


def timeit(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"{method.__name__} => {(end_time-start_time)*1000} ms")

        return result

    return wrapper


def download_one(url):
    """
    Downloads the specified URL and saves it to disk
    """

    req = urllib.request.urlopen(url)
    fullpath = Path(url)
    fname = fullpath.name
    fname_path = Path(__file__).parent.joinpath(fname)
    ext = fullpath.suffix

    if not ext:
        raise RuntimeError("URL does not contain an extension")

    with open(fname_path, "wb") as handle:
        while True:
            chunk = req.read(1024)
            if not chunk:
                break
            handle.write(chunk)

    msg = f"Finished downloading {fname}"
    return msg


@timeit
def download_all(urls):
    """
    Create a thread pool and download specified urls
    """

    futures_list = []
    results = []

    with ThreadPoolExecutor(max_workers=13) as executor:
        for url in urls:
            futures = executor.submit(download_one, url)
            futures_list.append(futures)

        for future in futures_list:
            try:
                result = future.result(timeout=60)
                results.append(result)
            except Exception as exc:
                results.append(None)
                print(exc)
    return results


if __name__ == "__main__":
    urls = (
        "http://www.irs.gov/pub/irs-pdf/f1040.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040",
        "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf",
    )

    results = download_all(urls)
    for result in results:
        print(result)
