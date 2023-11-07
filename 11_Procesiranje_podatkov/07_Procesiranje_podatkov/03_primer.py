def moja_funkcija(x):
    return x + 1


print((lambda x: x + 1)(2))


def soritraj():
    unsorted = [("b", 6), ("a", 10), ("d", 0), ("c", 4)]
    print(sorted(unsorted, key=lambda x: x[1]))


if __name__ == "__main__":
    soritraj()
