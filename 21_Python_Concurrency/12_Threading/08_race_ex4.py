import threading
import time
import random

counter = 0


def fuzz():
    time.sleep(random.random())


def worker():
    "My job is to increment the counter and print the current count"
    global counter

    fuzz()
    old_counter = counter
    fuzz()
    counter = old_counter + 1
    fuzz()
    print("The count is %d" % counter, end="")
    fuzz()
    print()
    fuzz()
    print("---------------", end="")
    fuzz()


print("Starting up")
fuzz()
for i in range(10):
    threading.Thread(target=worker).start()
    fuzz()
print("Finishing up")
fuzz()
