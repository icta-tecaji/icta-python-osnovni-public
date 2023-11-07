def izracun_davka(cena: float) -> float:
    TAX_RATE = 0.08
    return round(cena * (1 + TAX_RATE), 2)


def for_loop_list():
    squares = []
    for i in range(10):
        squares.append(i * i)
    print(squares)


def lc_list():
    squares = [i * i for i in range(10)]
    print(squares)


def for_loop_list_davki():
    txns = [1.09, 23.56, 57.84, 4.56, 6.78]
    cena_z_davkom = []
    for cena in txns:
        cena_z_davkom.append(round(izracun_davka(cena), 2))
    print(cena_z_davkom)


def lc_list_davki():
    txns = [1.09, 23.56, 57.84, 4.56, 6.78]
    cena_z_davkom = [round(izracun_davka(cena), 2) for cena in txns]
    print(cena_z_davkom)


def map_list_davki():
    txns = [1.09, 23.56, 57.84, 4.56, 6.78]
    cena_z_davkom = list(map(izracun_davka, txns))
    print(cena_z_davkom)


def filtriranje_samoglasnikov():
    sentence = "the rocket came back from mars"
    vowels = [i.upper() for i in sentence if i in "aeiou"]
    print(vowels)


def is_consonant(letter: str) -> bool:
    vowels = "aeiou"
    return letter.isalpha() and letter.lower() not in vowels


def filtrianje_crk():
    sentence = "The rocket, who was named Ted, came back \
from Mars because he missed his friends."
    consonants = [i.lower() for i in sentence if is_consonant(i)]
    print(consonants)


def pogojno_spreminjanje_vrednosti():
    original_prices = [1.25, -9.45, 10.22, 3.78, -5.92, 1.16]
    prices = [i if i > 0 else 0 for i in original_prices]
    print(prices)


def get_price(price):
    return price if price > 0 else 0


def pogojno_spreminjanje_vrednosti_funkcija():
    original_prices = [1.25, -9.45, 10.22, 3.78, -5.92, 1.16]
    prices = [get_price(i) for i in original_prices]
    print(prices)


def dict_comp():
    squares = {i: i * i for i in range(10)}
    print(squares)


if __name__ == "__main__":
    # for_loop_list()
    # lc_list()
    # print("-------------------")
    # for_loop_list_davki()
    # map_list_davki()
    # for_loop_list_davki()
    # print("-------------------")
    # filtriranje_samoglasnikov()
    # filtrianje_crk()
    # print("-------------------")
    # pogojno_spreminjanje_vrednosti()
    # pogojno_spreminjanje_vrednosti_funkcija()

    dict_comp()
