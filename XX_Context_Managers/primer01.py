def osnovno_odpiranje_datoteke(path):
    # 1. odpiranje datoteke
    file_object = open(path)

    # 2. delo z datoteko
    print(file_object)
    # operacije nad datoteko

    # 3. zapiranje datoteke
    file_object.close()


def odpiranje_datoteke_brez_napake(path):
    # 1. odpiranje datoteke
    file_object = open(path)

    # 2. izvajamo operacije
    try:
        print(file_object)
        # operacije nad datoteko
    finally:
        # 3. zapiranje datoteke
        file_object.close()


def odpiranje_s_pomocjo_context_managerja(path):
    with open(path) as file_object:
        print(file_object)
        # operacije nad datoteko


if __name__ == "__main__":
    path = "data/hello.txt"
    osnovno_odpiranje_datoteke(path)
    odpiranje_datoteke_brez_napake(path)
    odpiranje_s_pomocjo_context_managerja(path)
