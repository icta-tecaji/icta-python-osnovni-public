from app.my_sum import my_sum


def test_sum():
    assert my_sum([1, 2, 3]) == 6, "Should be 6"


def test_tuple_sum():
    assert my_sum((1, 2, 3)) == 6, "Should be 6"
