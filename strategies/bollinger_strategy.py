
import numpy as np # type: ignore
from strategies.base import Strategy

class BollingerStrategy(Strategy):
    def __init__(self, period=20, num_std=2, vol_range=(1,5)):
        self.period  = period
        self.num_std = num_std
        self.vol_min, self.vol_max = vol_range
        self.prices = []

    def decide(self, trader_id, tick, price):
        self.prices.append(price)
        if len(self.prices) < self.period:
            return {"action": "hold", "volume": 0}

        window = self.prices[-self.period:]
        sma    = np.mean(window)
        std    = np.std(window)
        upper  = sma + self.num_std * std
        lower  = sma - self.num_std * std

        if price < lower:
            action = "buy"
        elif price > upper:
            action = "sell"
        else:
            action = "hold"

        volume = 0 if action == "hold" else self.vol_min
        return {"action": action, "volume": volume}
