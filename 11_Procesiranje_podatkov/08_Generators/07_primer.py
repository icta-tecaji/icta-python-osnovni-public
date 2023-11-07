"""
1. Reading Large Files
2. Generating an Infinite Sequence
3. Creating New Iteration Patterns with Generators
4. Creating Data Pipelines With Generators
"""


def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment


if __name__ == "__main__":
    # inf = infinite_sequence()
    # print(next(inf))
    # print(next(inf))

    print(list(frange(1, 10, 0.5)))
