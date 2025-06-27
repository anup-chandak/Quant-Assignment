
from strategies.llm_strategy import LLMStrategy 

class LLMEngine:
    def __init__(self, strategy_cls=LLMStrategy):
        self.strategy = strategy_cls()

    def decide(self, trader_id, tick, price):
        return self.strategy.decide(trader_id, tick, price)
