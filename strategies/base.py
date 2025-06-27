

from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def decide(self, trader_id: int, tick: int, price: float) -> dict:
        pass
