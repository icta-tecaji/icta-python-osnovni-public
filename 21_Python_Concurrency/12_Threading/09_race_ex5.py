import threading
import time
import random

counter = 0
counter_lock = threading.Lock()
printer_lock = threading.Lock()


def fuzz():
    time.sleep(random.random())


def worker():
    "My job is to increment the counter and print the current count"
    global counter
    with counter_lock:
        old_counter = counter
        counter = old_counter + 1
        with printer_lock:
            print("The count is %d" % counter)
            print()
            print("---------------")


with printer_lock:
    print("Starting up")


working_threads = []
for i in range(10):
    t = threading.Thread(target=worker)
    working_threads.append(t)
    t.start()

for t in working_threads:
    t.join()

with printer_lock:
    print("Finishing up")
