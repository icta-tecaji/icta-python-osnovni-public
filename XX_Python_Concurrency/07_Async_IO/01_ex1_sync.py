import queue


def task(name, work_queue: queue.Queue):
    while not work_queue.empty():
        count = work_queue.get()
        total = 0
        print(f"Task {name} running!")
        for x in range(count):
            total += 1
            yield
        print(f"Task {name} total: {total}")


def main():
    working_queue = queue.Queue()
    for work in [15, 10, 5, 2]:
        working_queue.put(work)

    tasks = [task("one", working_queue), task("two", working_queue)]

    done = False
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True


if __name__ == "__main__":
    main()
