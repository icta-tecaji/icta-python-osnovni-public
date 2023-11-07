import time

COUT = 50_000_000


def countdown(n):
    while n > 0:
        n -= 1


start = time.time()
countdown(COUT)
end = time.time()

print(f"Time taken in seconds: {end- start}")
