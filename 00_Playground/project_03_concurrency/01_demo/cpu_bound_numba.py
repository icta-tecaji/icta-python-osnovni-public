import time

from numba import jit


@jit
def cpu_bound(number):
    total_sum = 0
    for i in range(number):
        total_sum += i * i
    return total_sum


def find_sums(numbers):
    for number in numbers:
        cpu_bound(number)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(10)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")
