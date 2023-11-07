import sys
import cProfile

if __name__ == "__main__":
    nums_squared_lc = [i * 2 for i in range(1_000_000)]
    print(sys.getsizeof(nums_squared_lc))

    nums_squared_gc = (i ** 2 for i in range(1_000_000))
    print(sys.getsizeof(nums_squared_gc))

    print(cProfile.run("sum([i * 2 for i in range(1_000_000)])"))
    print(cProfile.run("sum((i * 2 for i in range(1_000_000)))"))
