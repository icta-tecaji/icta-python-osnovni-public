from app.palindrome import is_palindrome
import pytest


@pytest.mark.parametrize(
    "palindrome",
    [
        "",
        "a",
        "Bob",
        "Never odd or even",
        "Do geese see God?",
    ],
)
def test_is_palindrome(palindrome):
    assert is_palindrome(palindrome)


@pytest.mark.parametrize(
    "non_palindrome",
    [
        "abc",
        "abab",
    ],
)
def test_is_palindrome_not_palindrome(non_palindrome):
    assert not is_palindrome(non_palindrome)
