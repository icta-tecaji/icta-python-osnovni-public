class InsufficentAmount(Exception):
    pass


class Wallet:
    def __init__(self, initial_amount=0):
        self.blance = initial_amount

    def spend_cash(self, amount):
        if self.blance < amount:
            raise InsufficentAmount(f"Not enough money to spend: {self.blance}")
        self.blance -= amount

    def add_cash(self, amount):
        self.blance += amount


if __name__ == "__main__":
    moja_denarnica = Wallet(50)
    print(moja_denarnica.blance)
    moja_denarnica.spend_cash(40)
    print(moja_denarnica.blance)
    moja_denarnica.add_cash(100)
    print(moja_denarnica.blance)
