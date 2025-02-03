"""Python Threading Primer 01."""

import threading
import time


def task(sleep_time: int, message: str) -> None:
    """Task function."""
    local = threading.local()
    local.value = sleep_time
    time.sleep(sleep_time)
    print(
        f"[{threading.current_thread().name}][daemon={threading.current_thread().daemon}] {message} from the thread. Stored value: {local.value}"
    )


if __name__ == "__main__":
    print("This is the main thread.")
    thread_01 = threading.Thread(name="Primer1", target=task, args=(4, "I'm thread 1..."), daemon=False)
    thread_02 = threading.Thread(name="Primer2", target=task, args=(2, "I'm thread 2..."), daemon=False)
    thread_01.start()  # non blocking, returns immediately
    thread_02.start()  # non blocking, returns immediately
    print(f"[{threading.current_thread().name}] This is the main thread again.")
    print(f"[{threading.current_thread().name}] Waiting for the thread to finish.")
    thread_01.join()  # blocking, waits until the thread finishes
    thread_02.join()  # blocking, waits until the thread finishes
    print(f"[{threading.current_thread().name}] Thread has finished.")
