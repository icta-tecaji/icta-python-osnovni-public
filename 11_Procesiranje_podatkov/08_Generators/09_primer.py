def generator():
    for i in range(10):
        yield i
    for j in range(10, 20):
        yield j


def generator2():
    for i in range(10):
        yield i


def generator3():
    for j in range(10, 20):
        yield j


def generator_all():
    generators = [generator2(), generator3()]
    for gen in generators:
        yield from gen


if __name__ == "__main__":
    gen = generator_all()

    for a in gen:
        print(a)
