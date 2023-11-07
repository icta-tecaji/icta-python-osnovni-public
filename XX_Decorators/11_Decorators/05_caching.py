import functools
import pickle


def cache_results(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = (pickle.dumps(args), pickle.dumps(kwargs))
        if t not in cache:
            print(f"Caching NEW value for {func.__name__}: {args}, {kwargs}")
            cache[t] = func(*args, **kwargs)
        else:
            print(f"Using OLD value for {func.__name__}: {args}, {kwargs}")
        return cache[t]

    return wrapper


@cache_results
def add(a, b):
    return a + b


if __name__ == "__main__":
    print(add(2, 2))
    print(add(2, 2))
    print(add(2, 3))
    print(add(4, 2))
