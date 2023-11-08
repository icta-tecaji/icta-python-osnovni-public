from concurrent.futures import ThreadPoolExecutor
from time import sleep


def return_after_5_secs(message):
    sleep(5)
    return message


with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(return_after_5_secs, ("hello1", "hello2"))
    for result in results:
        print(result)
