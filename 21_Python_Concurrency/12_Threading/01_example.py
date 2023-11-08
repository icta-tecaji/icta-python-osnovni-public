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
    logging.info("MAIN: Before creating thread")
    t1 = threading.Thread(target=thread_function, args=(1,))
    logging.info("MAIN: Before starting thread")
    t1.start()
    logging.info("MAIN: Waiting thread to finish")
    logging.info("MAIN: all done!")
