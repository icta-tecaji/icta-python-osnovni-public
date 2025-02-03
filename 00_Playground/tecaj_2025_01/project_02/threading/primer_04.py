"""Python Threading Primer 01."""

import threading
import time

from loguru import logger

# Python Threading provides concurrency in Python with native threads.
# Each program is a process and has at least one thread that executes instructions for that process.
# The main thread is the default thread of a Python process.


def custom_exception_hook(args):
    """Custom exception hook."""
    logger.error(f"Exception occurred: {args.exc_value}")


# Example of Running a Function in a Thread With Arguments
def task(sleep_time: int, message: str) -> None:
    """Task function."""
    try:
        if threading.current_thread().name == "Primer1":
            raise ValueError("This is a test error.")
        if threading.current_thread().name == "Primer2":
            raise ZeroDivisionError("This is another test error.")
        time.sleep(sleep_time)
        print(f"[{threading.current_thread().name}][daemon={threading.current_thread().daemon}] {message} from the thread.")
    except ZeroDivisionError:
        logger.warning(f"ZeroDivisionError occurred in thread: {threading.current_thread().name}")


if __name__ == "__main__":
    print("This is the main thread.")
    threading.excepthook = custom_exception_hook
    thread_01 = threading.Thread(name="Primer1", target=task, args=(4, "I'm thread 1..."), daemon=False)
    thread_02 = threading.Thread(name="Primer2", target=task, args=(2, "I'm thread 2..."), daemon=False)
    thread_01.start()  # non blocking, returns immediately
    thread_02.start()  # non blocking, returns immediately
    print(f"[{threading.current_thread().name}] This is the main thread again.")
    print(f"[{threading.current_thread().name}] Waiting for the thread to finish.")
    thread_01.join()  # blocking, waits until the thread finishes
    thread_02.join()  # blocking, waits until the thread finishes
    print(f"[{threading.current_thread().name}] Thread has finished.")
