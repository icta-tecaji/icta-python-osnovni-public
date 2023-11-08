import hashlib
import time
from concurrent.futures import ProcessPoolExecutor
from functools import wraps


def timeit(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"{method.__name__} => {(end_time-start_time)*1000} ms")

        return result

    return wrapper


def hash_one(n):
    """A somewhat CPU-intensive task."""

    for i in range(1, n):
        hashlib.pbkdf2_hmac("sha256", b"password", b"salt", i * 10000)

    return f"done {n}"


@timeit
def hash_all(n):

    with ProcessPoolExecutor(max_workers=10) as executor:
        for arg, res in zip(range(n), executor.map(hash_one, range(n), chunksize=2)):
            print(arg, res)

    return "done"


if __name__ == "__main__":
    hash_all(10)
