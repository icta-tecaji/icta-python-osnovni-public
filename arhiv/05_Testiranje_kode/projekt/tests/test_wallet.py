from app.wallet import Wallet, InsufficentAmount
import pytest


@pytest.fixture
def empty_wallet():
    """Return an empty Wallet instance."""
    return Wallet()


@pytest.fixture
def my_wallet():
    """Return an Wallet instance with 100€."""
    return Wallet(100)


def test_default_initial_amount(empty_wallet):
    assert empty_wallet.blance == 0


def test_settign_initial_amount(my_wallet):
    assert my_wallet.blance == 100


def test_wallet_add_amount(my_wallet):
    my_wallet.add_cash(50)
    assert my_wallet.blance == 150


def test_wallet_spend_amount(my_wallet):
    my_wallet.spend_cash(50)
    assert my_wallet.blance == 50


def test_wallet_spend_amount_error(my_wallet):
    with pytest.raises(InsufficentAmount):
        my_wallet.spend_cash(150)


@pytest.mark.parametrize(
    "earned,spent,expected",
    [
        (30, 10, 20),
        (20, 2, 18),
    ],
)
def test_transactions(empty_wallet, earned, spent, expected):
    empty_wallet.add_cash(earned)
    empty_wallet.spend_cash(spent)
    assert empty_wallet.balance == expected
