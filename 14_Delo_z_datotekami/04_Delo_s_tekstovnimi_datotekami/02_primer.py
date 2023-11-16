from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def preberemo_celotno_datoteko(path: str) -> None:
    # preberemo celotno datoteko
    with open(path, "r", encoding="utf-8") as reader:
        vsebina = reader.read()
        print(vsebina)


def preberemo_doloceno_stevilo_bajtov(path: str) -> None:
    with open(path, "r", encoding="utf-8") as reader:
        vsebina = reader.read(4)
        print(vsebina)
        vsebina = reader.read(10)
        print(vsebina)

        _ = reader.read()

        vsebina = reader.read(10)
        print(vsebina)


def preberemo_posamezno_vrstico(path: str) -> None:
    with open(path, "r", encoding="utf-8") as reader:
        vrstica = reader.readline()
        print(vrstica)
        vrstica = reader.readline()
        print(vrstica)


def preberemo_vse_vrstice(path: str) -> None:
    with open(path, "r", encoding="utf-8") as reader:
        vrstice = reader.readlines()
        print(vrstice)
        print(type(vrstice))


if __name__ == "__main__":
    path = "data/test.txt"
    path = get_absolute_file_path(path)
    # preberemo_celotno_datoteko(full_path)
    # preberemo_doloceno_stevilo_bajtov(full_path)
    # preberemo_posamezno_vrstico(path)
    # preberemo_vse_vrstice(path)

    # with open(path, "r", encoding="utf-8") as reader:
    #     vrstice = reader.readlines()

    #     for vrstica in vrstice:
    #         if "TRACE" in vrstica:
    #             print(vrstica, end="")

    with open(path, "r", encoding="utf-8") as reader:
        for vrstica in reader:
            if "TRACE" in vrstica:
                print(vrstica, end="")
