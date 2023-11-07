from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


if __name__ == "__main__":
    # list comprehension
    lc_example = [n ** 2 for n in range(6)]
    print(lc_example)

    # generator expression
    gen_example = (n ** 2 for n in range(6))
    gen_example = (n ** 2 for n in range(6) if n >= 3)
    # print(next(gen_example))
    # print(next(gen_example))

    for val in gen_example:
        print(val)

    file_data_generator = (row for row in open(get_absolute_file_path("data/recipeData.csv"), encoding="ISO-8859-1"))
    print(next(file_data_generator))
    print(next(file_data_generator))
    print(next(file_data_generator))
