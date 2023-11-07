import time
from concurrent.futures import ThreadPoolExecutor


def get_tasks():
    return list(range(20))


def perform(number):
    time.sleep(1)
    return number * number


with ThreadPoolExecutor(max_workers=10) as executor:
    for arg, res in zip(get_tasks(), executor.map(perform, get_tasks())):
        print(f"The power of {arg} is {res}")
