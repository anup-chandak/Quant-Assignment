class Market:
    def __init__(self, init_price: float, impact: float = 0.2):
        self.current_price = init_price
        self.impact = impact
        self.price_history: list[float] = [init_price]

    def update_price(self, net_demand: int):
        new_price = max(0.01, self.current_price + self.impact * net_demand)
        self.current_price = new_price
        self.price_history.append(new_price)
