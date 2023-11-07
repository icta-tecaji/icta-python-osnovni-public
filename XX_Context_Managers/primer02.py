class Odpri:
    def __init__(self, path) -> None:
        self.path = path

    def __enter__(self):
        self.file = open(self.path)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


if __name__ == "__main__":
    path = "data/hello.txt"
    with Odpri(path) as file_object:
        print(file_object)

    print("Konec")
