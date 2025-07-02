import random

from resources      import TraderDb, MarketDb
from resourceAccess import TraderAccess, MarketAccess
from strategies     import strategy_map
from engines        import LLMEngine, MarketEngine
from entities       import Trader

class SimulationController:
    def __init__(self, num_traders, ticks, init_price, strategy_name, seed=None):
        self.num_traders = num_traders
        self.ticks       = ticks
        if seed is not None:
            random.seed(seed)

        self.trader_db     = TraderDb()
        self.market_db     = MarketDb(init_price=init_price)
        self.trader_access = TraderAccess(self.trader_db)
        self.market_access = MarketAccess(self.market_db)

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

    def run(self):
        for tid in range(self.num_traders):
            trader = Trader(id=tid, cash=1000.0, inventory=0)
            self.trader_access.db.CreateTrader(trader)

        price_history = self.market_engine.run_simulation()
        print("Price history:", [round(p, 2) for p in price_history])
        print(f"Simulation Completed: {self.num_traders} traders, {self.ticks} ticks.")


        price_history = self.market_engine.run_simulation()
        print("Price history:", [round(p, 2) for p in price_history])
        print(f"Simulation Completed: {self.num_traders} traders, {self.ticks} ticks.")
