import functools


def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("To se je zgodilo pred klicem funkcije!")
        func()
        print("To je po klicu funkcije!")

    return wrapper


def do_twice(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper


@do_twice
def say_hello(name):
    """Returns hello."""
    print(f"hello {name}!")
    return True


if __name__ == "__main__":
    print(say_hello("peter"))
    print(say_hello)
    print(say_hello.__name__)
    # print(help(say_hello))
