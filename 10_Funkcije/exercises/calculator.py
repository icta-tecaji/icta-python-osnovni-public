"""Calculator script. Supports only basic operations (+, -, *, /)."""

from __future__ import annotations


def calculator(x: float, y: float, *, operation: str = "+") -> float | None:
    """Support only basic operations (+, -, *, /)."""
    if operation == "+":
        return x + y

    if operation == "-":
        return x - y

    if operation == "*":
        return x * y

    if operation == "/":
        return x / y

    return None


def main() -> None:
    """Run main function."""
    print("Welcome to the calculator!")  # noqa: T201
    first = float(input("Please enter the first number: "))
    second = float(input("Please enter the second number: "))
    operation = input("Please enter the operation (+, -, *, /): ")
    result = calculator(first, second, operation=operation)
    if result is None:
        print("Invalid operation!")  # noqa: T201
    else:
        print(f"Result is: {result}")  # noqa: T201


if __name__ == "__main__":
    main()
