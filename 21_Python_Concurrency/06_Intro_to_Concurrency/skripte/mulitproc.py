import time
from multiprocessing import Pool

COUT = 50_000_000


def countdown(n):
    while n > 0:
        n -= 1


if __name__ == "__main__":
    pool = Pool(processes=2)
    start = time.time()
    m1 = pool.apply_async(countdown, [COUT // 2])
    m2 = pool.apply_async(countdown, [COUT // 2])
    pool.close()
    pool.join()
    end = time.time()

    print(f"Time taken in seconds: {end - start}")
