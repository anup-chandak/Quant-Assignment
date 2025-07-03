from resourceAccess.traderAccess import TraderAccess
from resourceAccess.marketAccess import MarketAccess
from entities.trader import Trader
from entities.market import Market

class MarketEngine:
    def __init__(self, trader_db, market_db, llm_engine, ticks: int = 50):
        self.trader_access = TraderAccess(trader_db)
        self.market_access = MarketAccess(market_db)
        self.llm_engine = llm_engine
        self.ticks = ticks

    def run_simulation(self) -> list[float]:
        market: Market = self.market_access.get_market()
        traders: list[Trader] = list(self.trader_access.db.traders.values())

        for tick in range(self.ticks):
            price = market.current_price
            net_demand = 0

            for trader in traders:
                dec = self.llm_engine.decide(trader.id, tick, price)
                action, vol = dec["action"], int(dec["volume"])

                if action == "buy" and trader.try_buy(vol, price):
                    net_demand += vol
                elif action == "sell" and trader.try_sell(vol, price):
                    net_demand -= vol

                trader.record_net_worth(price)

                self.trader_access.db.WriteTraderBalance(trader.id, trader.cash)
                self.trader_access.db.WriteTraderInventory(trader.id, trader.inventory)

            old_price = market.current_price
            market.update_price(net_demand)
            print(f"[Market] net={net_demand}, {old_price:.2f}→{market.current_price:.2f}")

            self.market_access.save_market(market)

        return market.price_history
