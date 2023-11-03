def captial_case(x: str):
    if not isinstance(x, str):
        raise TypeError("Please provide a string argument!")
    return x.capitalize()
