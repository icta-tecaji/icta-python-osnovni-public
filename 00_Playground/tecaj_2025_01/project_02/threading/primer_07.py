"""Python Threading Primer 01."""

import random
import threading
import time


# Thread Mutex Lock
# A mutex lock is used to protect critical sections of code from concurrent execution.
def task(lock, sleep_time: float) -> None:
    """Task function."""
    with lock:
        print(
            f"[{threading.current_thread().name}] Sleeping for {sleep_time} seconds. Acquiring the lock.",
        )
    time.sleep(sleep_time)


if __name__ == "__main__":
    print("This is the main thread.")
    lock = threading.Lock()
    threads = []
    start_time = time.time()
    for i in range(10):
        thread = threading.Thread(name=f"Primer{i}", target=task, args=(lock, random.random()), daemon=False)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"[{threading.current_thread().name}] All threads have finished in {time.time() - start_time} seconds.")
