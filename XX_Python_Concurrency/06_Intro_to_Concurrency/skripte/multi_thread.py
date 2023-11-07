import time
from threading import Thread

COUT = 50_000_000


def countdown(n):
    while n > 0:
        n -= 1


t1 = Thread(target=countdown, args=(COUT // 2,))
t2 = Thread(target=countdown, args=(COUT // 2,))
start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()

print(f"Time taken in seconds: {end- start}")
