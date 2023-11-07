from pathlib import Path


def countdown_function(num: int):
    print("Starting")
    while num > 0:
        return num
        num -= 1
    print("stop!")


def function_a():
    return "a"


def generator_a():
    yield "a"


def multigen():
    yield "a"
    yield "b"
    yield "c"


def countdown_generator(num: int):
    print("Starting")
    while num > 0:
        yield num
        num -= 1
    print("stop!")


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


def file_data_generator(file_name: str, encoding: str):
    with open(file_name, encoding=encoding) as f:
        for row in f:
            yield row


if __name__ == "__main__":
    # print(countdown_function(5))

    # print(function_a())

    # a = generator_a()
    # print(next(a))
    # # print(next(a))

    # mg = multigen()
    # print(next(mg))
    # print(next(mg))
    # print(next(mg))

    # mg = multigen()
    # for value in mg:
    #     print(value)

    # for count in countdown_generator(5):
    #     print(count)

    recept = file_data_generator(get_absolute_file_path("data/recipeData.csv"), "ISO-8859-1")
    print(next(recept))
    print(next(recept))
    print(next(recept))
