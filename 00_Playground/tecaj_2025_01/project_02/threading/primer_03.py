"""Python Threading Primer 01."""

import time
from threading import Thread

# Extend the Thread Class


class MyCustomThread(Thread):
    def __init__(self, sleep_time: int, message: str):
        super().__init__()
        self.sleep_time = sleep_time
        self.message = message
        self.result = None

    def run(self) -> None:
        """Task function."""
        time.sleep(self.sleep_time)
        print(f"[{thread.name}][daemon={thread.daemon}] {self.message} from the thread.")
        self.result = self.sleep_time * 2


if __name__ == "__main__":
    print("This is the main thread.")
    thread = MyCustomThread(4, "I'm thread 1...")
    thread.start()  # non blocking, returns immediately
    print("[MAIN] This is the main thread again.")
    print("[MAIN] Waiting for the thread to finish.")
    thread.join()  # blocking, waits until the thread finishes
    print(f"[MAIN] Thread has finished. Result: {thread.result}")
    print("[MAIN] Thread has finished.")
