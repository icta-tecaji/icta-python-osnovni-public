import functools
import time


class CalledTooOtfenError(Exception):
    pass


def once_per_n_seconds(n_seconds):
    def middle(func):
        last_invoked = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_invoked
            elapsed_time = time.perf_counter() - last_invoked
            if elapsed_time < n_seconds:
                raise CalledTooOtfenError(
                    f"Only {elapsed_time:.2f} seconds passed instead of {n_seconds} seconds.",
                )
            last_invoked = time.perf_counter()
            return func(*args, **kwargs)

        return wrapper

    return middle


@once_per_n_seconds(3)
def add(a, b):
    return a + b


if __name__ == "__main__":
    print(add(2, 2))
    time.sleep(4)
    print(add(2, 2))
