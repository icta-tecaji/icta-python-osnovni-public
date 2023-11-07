import time
from tasks import make_request
from concurrent.futures import ThreadPoolExecutor, wait


def main():
    futures = []

    with ThreadPoolExecutor() as executor:
        for num in range(1, 101):
            futures.append(executor.submit(make_request, num))

    wait(futures)


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time}")
