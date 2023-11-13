import re

RE_WORD = re.compile(r"\w+")


class Worditerator:
    def __init__(self, text) -> None:
        self.words = RE_WORD.findall(text)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word


if __name__ == "__main__":
    for word in Worditerator("Danes je sončen dan."):
        print(word)
