# resourceAccess/marketAccess.py
from resources.MarketDb import MarketDb

class MarketAccess:
    def __init__(self, market_db: MarketDb):
        self.db = market_db

    def get_current_price(self):
        return self.db.ReadPrice()

    def set_price(self, new_price):
        self.db.WritePrice(new_price)
