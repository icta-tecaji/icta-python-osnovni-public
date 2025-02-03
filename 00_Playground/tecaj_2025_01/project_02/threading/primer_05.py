import random
import threading
import time

counter = 0
counter_lock = threading.Lock()
printer_lock = threading.Lock()


def fuzz():
    time.sleep(random.random())


def worker():
    """My job is to increment the counter and print the current count"""
    global counter
    fuzz()

    with counter_lock:
        counter += 1
        with printer_lock:
            fuzz()
            fuzz()
            print("The count is %d" % counter)
            fuzz()
            print("---------------")
            fuzz()


with printer_lock:
    print("Starting up")
fuzz()

working_threads = []

for i in range(10):
    t = threading.Thread(target=worker)
    working_threads.append(t)
    t.start()

for t in working_threads:
    t.join()


with printer_lock:
    print("Finishing up")

fuzz()
