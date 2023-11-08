import time
from tasks import get_prime_numbers


def main():
    for num in range(1000, 10000):
        get_prime_numbers(num)


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time}")
