"""Python Threading Primer 01."""

import time
from threading import Thread

# Python Threading provides concurrency in Python with native threads.
# Each program is a process and has at least one thread that executes instructions for that process.
# The main thread is the default thread of a Python process.


# Example of Running a Function in a Thread With Arguments
def task(sleep_time: int, message: str) -> None:
    """Task function."""
    time.sleep(sleep_time)
    print(f"{message} from the thread.")


if __name__ == "__main__":
    print("This is the main thread.")
    thread = Thread(target=task, args=(4, "I'm thread 1..."))
    thread.start()  # non blocking, returns immediately
    print("This is the main thread again.")
    print("Waiting for the thread to finish.")
    thread.join()  # blocking, waits until the thread finishes
    print("Thread has finished.")
