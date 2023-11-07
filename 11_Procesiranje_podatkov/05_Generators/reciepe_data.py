beer_data = "data/recipeData.csv"

with open(beer_data, "r", encoding="ISO-8859-1") as input_file:
    lines = (line for line in input_file)
    lists = (line.split(",") for line in lines)
    columns_names = next(lists)
    data_dicts = (dict(zip(columns_names, data)) for data in lists)

    total_boil_time = 0
    for beer in data_dicts:
        total_boil_time += int(beer["BoilTime"])

    print(total_boil_time)
