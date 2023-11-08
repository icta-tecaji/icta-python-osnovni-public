from multiprocessing import Pool


def doubler(number):
    return number * 2

if __name__ == '__main__':
    with Pool(processes=2) as pool:
        result = pool.apply_async(doubler, (25,))
        print(result.get(timeout=1))