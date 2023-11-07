def open_test_wrong():
    my_file = open("data/hello.txt", "w")
    print(my_file.closed)
    my_file.write("Heeellloo")
    print(45 / 0)
    my_file.close()
    print(my_file.closed)
    my_file.write("Heeellloo")


def open_test_exceptions():
    my_file = open("data/hello.txt", "w")
    try:
        print(my_file.closed)
        my_file.write("Heeellloo")
        print(45 / 0)
    finally:
        my_file.close()
    print(my_file.closed)
    my_file.write("Heeellloo")


def open_file_context():
    with open("data/hello.txt", "w") as my_file:
        print(my_file.closed)
        my_file.write("Heeellloo")
        print(45 / 0)
    print(my_file.closed)


if __name__ == "__main__":
    open_file_context()
