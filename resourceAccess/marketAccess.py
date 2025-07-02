
from entities.market import Market
from resources.MarketDb import MarketDb

class MarketAccess:
    def __init__(self, market_db: MarketDb):
        self.db = market_db

    def get_market(self) -> Market:
        price = self.db.ReadPrice()
        return Market(init_price=price)

    def save_market(self, market: Market) -> None:
        self.db.WritePrice(market.current_price)

    def get_current_price(self) -> float:
        return self.db.ReadPrice()

    def set_price(self, new_price: float) -> None:
        self.db.WritePrice(new_price)
