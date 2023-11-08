import math
import time


@profile
def f1(degrees):
    return math.cos(degrees)


@profile
def f2(degrees):
    e = 2.718281828459045
    n = 10000000
    while n > 0:
        n -= 1
    return ((e ** (degrees * 1j) + e ** -(degrees * 1j)) / 2).real


if __name__ == "__main__":
    f1(10)
    f2(20)
