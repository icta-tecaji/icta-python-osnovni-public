import re


def raw_strings_examples():
    print("Hello World")
    print("Hello\t World")
    print("Hello World in \\n!")
    print("Hello\b\b\b World")
    print("Hello World in \\n!")
    # raw string
    print(r"Hello World in \n!")


def match_string(text: str):
    # If zero or more characters at the beginning of string match this regular expression, return a corresponding match object.
    result = re.match(r"Exception", text)
    print(result)
    print(result.group())  # Return the string matched by the RE
    print(result.start())  # Return the starting position of the match
    print(result.end())  # Return the ending position of the match
    print(result.span())  # Return a tuple containing the (start, end) positions of the match

    if re.match(r"ffdException", text):
        print("Najdeno")
    else:
        print("ni!")


def search_string(text: str):
    # Scan through string looking for the first location where the regular expression pattern produces a match, and return a corresponding match object.
    result = re.search(r"one", text)
    print(result)

    print(result.group())  # Return the string matched by the RE
    print(result.start())  # Return the starting position of the match
    print(result.end())  # Return the ending position of the match
    print(result.span())  # Return a tuple containing the (start, end) positions of the match

    if re.search(r"here", text):
        print("Text found!")
    else:
        print("Not fonud!")


def findall_string(text: str):
    # Find all matches of a pattern.
    result = re.findall(r"one", text)
    print(result)


def finditer_string(text: str):
    result = re.finditer(r"one", text)
    print(result)

    for match in result:
        print(match)
        print(match.group())


def split_string(text: str):
    result = re.split(r"\.", text)
    print(result)


def sub_string(text: str):
    result = re.sub(r"one", "ena", text)
    print(result)


if __name__ == "__main__":
    # raw_strings_examples()
    text = """Exception one raised when a string passed to one. of the functions here is not a valid regular
    expression (for example, it might contain unmatched parentheses) or when some. other error occurs
    during compilation or matching. It is never an error if a string contains no match for a pattern.
    The error instance has the following additional attributes one.
    """

    # match_string(text)
    # search_string(text)
    # findall_string(text)
    # finditer_string(text)
    # split_string(text)
    sub_string(text)
