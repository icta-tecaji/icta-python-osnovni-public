import re
from typing import List

RE_WORD = re.compile(r"\w+")


class SentenceIterator:
    def __init__(self, text: str) -> None:
        self.words: List[str] = RE_WORD.findall("Danes je lep dan.")
        self.index: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()

        self.index += 1
        return word


class Doubler:
    def __init__(self) -> None:
        self.number = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.number += 1
        return self.number * self.number


if __name__ == "__main__":
    # sentence = SentenceIterator("Danes je lep dan.")

    # for word in sentence:
    #     print(word)

    doubler = Doubler()
    count = 0

    for number in Doubler():
        print(number)
        if count > 5:
            break
        count += 1
