
class MarketDb:
    def __init__(self, init_price=100.0):
        self.price = init_price

    def ReadPrice(self):
        return self.price

    def WritePrice(self, new_price):
        self.price = new_price
