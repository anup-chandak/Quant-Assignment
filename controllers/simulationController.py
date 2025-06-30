import random
from resources.TraderDb import TraderDb
from resources.MarketDb import MarketDb
from resourceAccess.traderAccess import TraderAccess
from resourceAccess.marketAccess import MarketAccess
from engines.llm_engine import LLMEngine
from engines.market_engine import MarketEngine
from entities.trader import Trader

from strategies.llm_strategy       import LLMStrategy
from strategies.random_strategy    import RandomStrategy
from strategies.rsi_strategy       import RSIStrategy
from strategies.bollinger_strategy import BollingerStrategy

class SimulationController:
    def __init__(
        self,
        num_traders: int,
        ticks: int,
        init_price: float,
        strategy_name: str,
        seed: int | None = None,
    ) -> None:
        self.num_traders = num_traders
        self.ticks       = ticks

        
        if seed is not None:
            random.seed(seed)

        
        self.trader_db     = TraderDb()
        self.market_db     = MarketDb(init_price=init_price)
        self.trader_access = TraderAccess(self.trader_db)
        self.market_access = MarketAccess(self.market_db)

        
        

        strategy_map = {
            "llm":       LLMStrategy,
            "random":    RandomStrategy,
            "rsi":       RSIStrategy,
            "bollinger": BollingerStrategy,
        }
        if strategy_name not in strategy_map:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy_cls = strategy_map[strategy_name]
        self.strategy_engine = LLMEngine(strategy_cls)

        
        self.market_engine = MarketEngine(
            self.trader_db,       
            self.market_db,       
            self.strategy_engine, 
            self.ticks            
        )

    def run(self) -> None:
        for tid in range(self.num_traders):
            trader = Trader(id=tid, cash=1000.0, inventory=0)
            self.trader_access.db.CreateTrader(trader)

        price_history = self.market_engine.run_simulation()
        print("Price history:", [round(p, 2) for p in price_history])
        print(f"Simulation Completed: {self.num_traders} traders, {self.ticks} ticks.")
