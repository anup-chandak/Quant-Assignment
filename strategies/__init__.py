from .llm_strategy       import LLMStrategy
from .random_strategy    import RandomStrategy
from .rsi_strategy       import RSIStrategy
from .bollinger_strategy import BollingerStrategy

strategy_map = {
    "llm":       LLMStrategy,
    "random":    RandomStrategy,
    "rsi":       RSIStrategy,
    "bollinger": BollingerStrategy,
}

__all__ = ["strategy_map"]
