import queue
import random
import threading
import time

from loguru import logger


def producer(queue, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        message = random.randint(1, 101)
        logger.debug(f"Producer got message: {message}")
        queue.put(message)

    logger.warning("Producer received event. Exiting")


def consumer(queue, event):
    """Pretend we're saving a number in the database."""
    current_thread = threading.current_thread()
    while not event.is_set() or not queue.empty():
        message = queue.get()
        time.sleep(0.2)
        logger.debug(f"[{current_thread.name}] Consumer storing message: {message}, size: {queue.qsize()}")

    logger.warning(f"[{current_thread.name}] Consumer received event. Exiting")


if __name__ == "__main__":
    logger.info("Starting the pipeline")
    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()

    thread_producer = threading.Thread(target=producer, args=(pipeline, event))
    thread_consumer1 = threading.Thread(target=consumer, args=(pipeline, event), name="Consumer 1")
    thread_consumer2 = threading.Thread(target=consumer, args=(pipeline, event), name="Consumer 2")
    thread_producer.start()
    thread_consumer1.start()
    thread_consumer2.start()
    time.sleep(0.1)
    logger.info("Main: about to set event")
    event.set()
