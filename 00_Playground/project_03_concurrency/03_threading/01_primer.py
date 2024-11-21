import threading
import time

from loguru import logger

# create a local instance
local = threading.local()


class MyTaskThread(threading.Thread):
    def run(self):
        time.sleep(1)
        current_thread = threading.current_thread()
        print(f"[{current_thread.name}][daemon={current_thread.daemon}] This is from MyTaskThread")
        self.value = 99


def custom_error_handler(args):
    logger.error(f"Thread failed {args.exc_value}")


def task(sleep_time, message, value):
    try:
        current_thread = threading.current_thread()
        local.value = value
        print(f"[{current_thread.name}][daemon={current_thread.daemon}] Starting....")
        time.sleep(sleep_time)
        # raise Exception("This is an error.")
        print(f"[{current_thread.name}][daemon={current_thread.daemon}] {message}, local value: {local.value}")
    except ValueError as e:
        print(e)


def daemon_job(sleep_time):
    while True:
        print("DEAMON: I am running.")
        time.sleep(sleep_time)


print("This is run from the main thread.")
threading.excepthook = custom_error_handler
thread_1 = threading.Thread(target=task, args=(1.5, "This is run from another thread 1.", 1), name="Moj task 1")
thread_2 = threading.Thread(target=task, args=(2, "This is run from another thread 2.", 2), name="Moj task 2")
print(thread_1.is_alive())
thread_1.start()
thread_2.start()
print(thread_1.is_alive())
thread_daemon = threading.Thread(target=daemon_job, args=(0.3,), daemon=True)
thread_daemon.start()
thread_class = MyTaskThread()
thread_class.start()

print(f"Currently running threads: {threading.active_count()}")
print(f"Main thread: {threading.current_thread().name}")

print("This is run from the main thread after starting the thread.")
# wait for the thread to finish
thread_1.join()
thread_2.join()
print(thread_1.is_alive())
thread_class.join()

print(f"MyTaskThread value: {thread_class.value}")
print("The program is done.")
