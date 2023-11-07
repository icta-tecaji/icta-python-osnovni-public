import time
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor


def get_tasks():
    return list(range(20))


def perform(number):
    time.sleep(1)
    return number * number


with ThreadPoolExecutor(max_workers=10) as executor:
    futures_set = {executor.submit(perform, task): task for task in get_tasks()}

    for fut in futures.as_completed(futures_set):
        original_task = futures_set[fut]
        print(f"The power of {original_task} is {fut.result()}")
