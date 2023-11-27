import functools
import time


def logtime(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        print(
            f"[{time.time()}] Function {func.__name__} took {total_time:.2f} seconds.",
        )
        return result

    return wrapper


@logtime
def waste_time():
    for _ in range(10):
        sum([i**2 for i in range(80_000)])


if __name__ == "__main__":
    for _ in range(5):
        waste_time()
