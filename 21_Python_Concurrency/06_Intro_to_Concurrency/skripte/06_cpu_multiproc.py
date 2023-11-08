import multiprocessing
import time
from multiprocessing import cpu_count

from tasks import get_prime_numbers


def main():
    with multiprocessing.Pool(cpu_count() - 1) as proc:
        proc.starmap(get_prime_numbers, zip(range(1000, 10000)))
        proc.close()
        proc.join()


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time}")
