

class Trader:
    def __init__(self, id: int, cash: float, inventory: float):
        self.id = id
        self.cash = cash
        self.inventory = inventory
        self.net_worth_history: list[float] = []

    def buy(self, volume: int, price: float) -> bool:
        cost = volume * price
        if cost > self.cash:
            return False
        self.cash -= cost
        self.inventory += volume
        return True

    def sell(self, volume: int, price: float) -> bool:
        if volume > self.inventory:
            return False
        self.inventory -= volume
        self.cash += volume * price
        return True

    def record_net_worth(self, price: float):
        self.net_worth_history.append(self.cash + self.inventory * price)
