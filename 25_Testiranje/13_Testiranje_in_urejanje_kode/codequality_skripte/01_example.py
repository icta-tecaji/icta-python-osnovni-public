def option1():
    numbers = []

    while True:
        answer = input("Enter a number: ")
        if answer != "quit":
            numbers.append(answer)
        else:
            break

    print("Numbers: %s" % numbers)


def option2():
    numbers = []

    while (answer := input("Enter a number: ")) != "quit":
        numbers.append(answer)

    print(f"Numbers: {numbers}")


def option3():
    numbers = []

    while True:
        answer = input("Enter a number: ")
        if answer == "quit":
            break
        numbers.append(answer)

    print(f"Numbers: {numbers}")


if __name__ == "__main__":
    option2()
