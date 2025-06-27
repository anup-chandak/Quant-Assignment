
class Trader:
    def __init__(self, id: int, cash: float, inventory: float):
        self.id = id
        self.cash = cash
        self.inventory = inventory
        self.net_worth_history: list[float] = []

    def record_net_worth(self, price: float):
        nw = self.cash + self.inventory * price
        self.net_worth_history.append(nw)
