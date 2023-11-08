from concurrent.futures import ThreadPoolExecutor
from time import sleep


def return_after_5_secs(message):
    sleep(5)
    return message


pool = ThreadPoolExecutor(3)

future1 = pool.submit(return_after_5_secs, ("hello1"))
future2 = pool.submit(return_after_5_secs, ("hello2"))

print(future1.done())
sleep(6)
print(future1.done())

print(f"Resutl 1: {future1.result()}")
print(f"Resutl 2: {future2.result()}")
pool.shutdown()
