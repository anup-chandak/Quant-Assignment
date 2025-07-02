
class Market:
    def __init__(self, init_price: float):
        self.current_price = init_price
        self.price_history: list[float] = [init_price]

    def update_price(self, net_demand: int, impact: float = 0.2):
        new_price = max(0.01, self.current_price + impact * net_demand)
        self.current_price = new_price
        self.price_history.append(new_price)
