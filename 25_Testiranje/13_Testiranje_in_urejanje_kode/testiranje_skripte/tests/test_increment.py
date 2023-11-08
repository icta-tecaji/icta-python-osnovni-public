from app.increment import increment
from hypothesis import given
import hypothesis.strategies as st


@given(st.integers())
def test_add_one(num):
    assert increment(num) == (num + 1)
