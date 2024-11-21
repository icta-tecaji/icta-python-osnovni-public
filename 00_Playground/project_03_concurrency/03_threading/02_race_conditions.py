import random
import threading
import time

from loguru import logger

counter = 0
FUZZ = True

counter_lock = threading.Lock()


def fuzz():
    if FUZZ:
        time.sleep(random.random())


logger.info("Starting up")


def worker():
    global counter
    with counter_lock:
        old_counter = counter
        counter = old_counter + 1
        time.sleep(0.5)
        logger.info(f"The count is {counter}")
        logger.info("----------")


threads = []

for i in range(10):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

# wait for the threads to finish

for thread in threads:
    thread.join()

logger.success(f"The program is done. The final count is {counter}")
