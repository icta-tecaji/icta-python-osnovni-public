import time
from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import cpu_count

from tasks import get_prime_numbers


def main():
    futures = []

    with ProcessPoolExecutor(cpu_count() - 1) as executor:
        for num in range(1000, 10000):
            futures.append(executor.submit(get_prime_numbers, num))

    wait(futures)


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time}")
