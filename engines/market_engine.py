from resourceAccess.traderAccess import TraderAccess
from resourceAccess.marketAccess import MarketAccess


class MarketEngine:
    def __init__(self, trader_db, market_db, llm_engine, ticks=50):
        self.trader_access = TraderAccess(trader_db)
        self.market_access = MarketAccess(market_db)
        self.llm_engine    = llm_engine
        self.ticks         = ticks

    def run_simulation(self):
        price_history = []
        for tick in range(self.ticks):
            price = self.market_access.get_current_price()
            price_history.append(price)
            self.net_demand = 0

            for trader in self.trader_access.db.traders.values():
                dec = self.llm_engine.decide(trader.id, tick, price)
                action, vol = dec["action"], int(dec["volume"])
                if action == "buy":  self._buy(trader.id, vol, price)
                if action == "sell": self._sell(trader.id, vol, price)

            self._update_market()

        return price_history

    def _buy(self, tid, vol, price):
        cost = vol * price
        if self.trader_access.get_balance(tid) >= cost:
            self.trader_access.decrease_balance(tid, cost)
            self.trader_access.increase_inventory(tid, vol)
            self.net_demand += vol

    def _sell(self, tid, vol, price):
        if self.trader_access.get_inventory(tid) >= vol:
            rev = vol * price
            self.trader_access.decrease_inventory(tid, vol)
            self.trader_access.increase_balance(tid, rev)
            self.net_demand -= vol

    def _update_market(self):
        impact = 0.2
        old   = self.market_access.get_current_price()
        new   = max(0.01, old + impact * self.net_demand)
        print(f"[Market] net={self.net_demand}, {old:.2f}→{new:.2f}")
        self.market_access.set_price(new)
