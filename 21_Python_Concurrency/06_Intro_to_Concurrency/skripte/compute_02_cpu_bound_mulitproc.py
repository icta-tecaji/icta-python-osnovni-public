import multiprocessing
import time


def cpu_bound(number: int):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(10)]
    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Run in {duration} seconds.")
