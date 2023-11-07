import time


def follow(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    bytes_sum = 0
    with open("access-log") as logfile:
        for line in follow(logfile):
            bytes_part = line.rsplit(None, 1)[1]
            if bytes_part != "-":
                bytes_sum += int(bytes_part)
            print(f"Current total traffic: {bytes_sum/1024/1024:.3} MB")
