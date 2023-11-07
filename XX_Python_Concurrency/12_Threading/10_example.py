import logging
import queue
import threading
import time
import random


def producer(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info(f"Produced message: {message}")
        queue.put(message)

    logging.info("Producer event recieved. Exiting.")


def consumer(queue: queue.Queue, event):
    while not event.is_set() or not queue.empty():
        message = queue.get()
        logging.info(f"Consumer message: {message}. In queue: {queue.qsize()}")

    logging.info("Consumer event recieved. Exiting.")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()

    t1 = threading.Thread(target=producer, args=(pipeline, event))
    t2 = threading.Thread(target=consumer, args=(pipeline, event))

    t1.start()
    t2.start()
    time.sleep(0.1)
    logging.info("Main: about to set event")
    event.set()

    t1.join()
    t2.join()
