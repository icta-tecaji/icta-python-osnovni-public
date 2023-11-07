import time


def follow(file_object):
    file_object.seek(0, 2)
    while True:
        line = file_object.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    with open("access-log") as log_file:
        for line in follow(log_file):
            print(line, end="")
