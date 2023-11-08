from concurrent.futures import ThreadPoolExecutor, wait
from time import sleep
from random import randint


def return_after_5_secs(num):
    sleep(randint(1, 5))
    if num == 3:
        raise ValueError
    return f"Return of {num}"


pool = ThreadPoolExecutor(5)
futures = []

for x in range(5):
    futures.append(pool.submit(return_after_5_secs, x))

done_futures = wait(futures)

print(done_futures.done)

for df in done_futures.done:
    try:
        print(df.result())
    except ValueError as e:
        print("Error")
