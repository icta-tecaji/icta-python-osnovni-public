from pathlib import Path


def get_absolute_file_path(relative_path: str) -> str:
    """
    This function return the absulute path of the provided relative path.
    """
    return str(Path(__file__).parent.joinpath(relative_path))


if __name__ == "__main__":
    beer_data = get_absolute_file_path("data/recipeData.csv")
    lines = (row for row in open(beer_data, encoding="ISO-8859-1"))
    lists_of_elements = (line.split(",") for line in lines)
    # shranimo imena stolpcev
    columns_names = next(lists_of_elements)
    # spremenimo vrednosti v splovarje
    beerdicts = (dict(zip(columns_names, line)) for line in lists_of_elements)

    beer_counts = {}
    for beer in beerdicts:
        if beer["Style"] not in beer_counts:
            beer_counts[beer["Style"]] = 1
        else:
            beer_counts[beer["Style"]] += 1

    # print(beer_counts)
    max_style = max(beer_counts, key=beer_counts.get)
    print(max_style, beer_counts[max_style])
