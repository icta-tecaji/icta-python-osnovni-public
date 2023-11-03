def get_data(a):
    print("get_data deluje ", a)
    return a


STATUS = "danes"
print("VREDNOST modul __name__: ", __name__)
if __name__ == "__main__":
    print("to je zelo uporaben modul")
    get_data("iz modula")
