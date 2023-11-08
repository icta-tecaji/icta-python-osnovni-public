import logging
import threading
import time


def thread_function(name):
    logging.info(f"Thread {name} strating!")
    time.sleep(2)
    logging.info(f"Thread {name} stopping!")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    threads = []

    for index in range(4):
        logging.info(f"MAIN: Create and start thread {index}")
        t = threading.Thread(target=thread_function, args=(index,))
        threads.append(t)
        t.start()

    for index, thread in enumerate(threads):
        logging.info(f"MAIN: Before joining thread: {index}")
        thread.join()
        logging.info(f"MAIN: thread {index} done.")

    logging.info("MAIN: all done!")
