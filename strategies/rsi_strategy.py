
import numpy as np # type: ignore
from strategies.base import Strategy

class RSIStrategy(Strategy):
    def __init__(self, period=14, vol_range=(1,5)):
        self.period = period
        self.vol_min, self.vol_max = vol_range
        self.prices = []

    def decide(self, trader_id, tick, price):
        self.prices.append(price)
        if len(self.prices) < self.period + 1:
            return {"action": "hold", "volume": 0}

        window = self.prices[-(self.period+1):]
        deltas = np.diff(window)
        gains  = deltas[deltas > 0].sum() / self.period
        losses = -deltas[deltas < 0].sum() / self.period
        rs     = gains / (losses or 1e-6)
        rsi    = 100 - (100 / (1 + rs))

        if rsi < 30:
            action = "buy"
        elif rsi > 70:
            action = "sell"
        else:
            action = "hold"

        volume = 0 if action == "hold" else self.vol_min
        return {"action": action, "volume": volume}
