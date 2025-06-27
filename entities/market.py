
class Market:
    def __init__(self, init_price: float):
        self.current_price = init_price
        self.price_history: list[float] = [init_price]

    def update_price(self, new_price: float):
        self.current_price = new_price
        self.price_history.append(new_price)
