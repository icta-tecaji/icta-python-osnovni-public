import time
from numba import jit


@jit
def cpu_bound(number: int):
    total_sum = 0
    for i in range(number):
        total_sum += i * i
    print(total_sum)
    return total_sum


def find_sums(numbers):
    for number in numbers:
        cpu_bound(number)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(1000)]
    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Run in {duration} seconds.")
