if __name__ == "__main__":
    with open("access-log") as logfile:
        bytecolumn = (line.rsplit(None, 1)[1] for line in logfile)
        bytes_sent = (int(x) for x in bytecolumn if x != "-")
        print(f"Total: {sum(bytes_sent)/1024/1024} MB")
