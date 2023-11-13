class Doubler:
    def __init__(self) -> None:
        self.number = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.number += 1
        return self.number**2


if __name__ == "__main__":
    doubler = Doubler()
    count = 0

    for number in doubler:
        print(number)
        if count > 10:
            break
        count += 1
