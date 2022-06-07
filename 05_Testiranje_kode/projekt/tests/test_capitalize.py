import pytest
from app.capitalize import captial_case


def test_capital_case():
    assert captial_case("vreme") == "Vreme"


def test_capital_case_int():
    with pytest.raises(TypeError):
        captial_case(123)
