import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    inputs = list(range(10))
    print('Input   :', inputs)

    builtin_outputs = map(do_calculation, inputs)
    print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count()
    
    with multiprocessing.Pool(processes=pool_size, initializer=start_process,) as pool:
        pool_outputs = pool.map(do_calculation, inputs)

    print('Pool    :', pool_outputs)