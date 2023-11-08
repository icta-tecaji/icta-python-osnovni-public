import multiprocessing
import sys

def worker_with(stream):
    stream.write('Lock acquired via with\n')


def worker_no_with(stream):
    stream.write('Lock acquired directly\n')
        
        
if __name__ == '__main__':
    w = multiprocessing.Process(
        target=worker_with,
        args=(sys.stdout,),
    )

    nw = multiprocessing.Process(
        target=worker_no_with,
        args=(sys.stdout,),
    )

    w.start()
    nw.start()

    w.join()
    nw.join()