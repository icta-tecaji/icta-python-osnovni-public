class ManagedFile:
    def __init__(self, name: str, mode: str) -> None:
        self.name: str = name
        self.mode: str = mode

    def __enter__(self):
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exc_type", exc_type, type(exc_type))
        print("exc_val", exc_val, type(exc_val))
        print("exc_val", exc_tb, type(exc_tb))

        if self.file:
            self.file.close()


class ReversePrinter:
    def __init__(self, duplicator: bool = False) -> None:
        self.duplicator: bool = duplicator

    def __enter__(self):
        import sys

        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write

    def reverse_write(self, text: str):
        if self.duplicator:
            self.original_write(text[::-1] * 2)
        else:
            self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys

        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("please don't devide by zero")
            return True


if __name__ == "__main__":
    # with ManagedFile("data/hello.txt", "w") as my_file:
    #     my_file.write("test")
    #     print(3443 / 0)

    print("to je pravilen text")
    with ReversePrinter(duplicator=False):
        print("to je obraten text")
        print(6 / 0)
        print("to je obraten text")
    print("to je pravilen text")
