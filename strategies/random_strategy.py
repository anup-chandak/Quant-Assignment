
import random
from strategies.base import Strategy

class RandomStrategy(Strategy):
    def __init__(self, vol_range=(1,5)):
        self.vol_min, self.vol_max = vol_range

    def decide(self, trader_id, tick, price):
        r = random.random()
        if r < 0.4:
            action = "buy"
        elif r < 0.8:
            action = "sell"
        else:
            action = "hold"

        volume = 0 if action == "hold" else random.randint(self.vol_min, self.vol_max)
        return {"action": action, "volume": volume}
