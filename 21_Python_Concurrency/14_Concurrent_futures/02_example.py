import chunk
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import sleep


def return_after_5_secs(message):
    sleep(5)
    return message


with ProcessPoolExecutor(max_workers=3, chunk_size=2) as executor:
    results = executor.map(return_after_5_secs, ("hello1", "hello2"))
    for result in results:
        print(result)
