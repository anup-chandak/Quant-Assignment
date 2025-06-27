# resourceAccess/traderAccess.py
from resources.TraderDb import TraderDb

class TraderAccess:
    def __init__(self, trader_db: TraderDb):
        self.db = trader_db

    def create_trader(self, trader):
        self.db.CreateTrader(trader)

    def get_balance(self, trader_id):
        return self.db.ReadTraderBalance(trader_id)

    def get_inventory(self, trader_id):
        return self.db.ReadTraderInventory(trader_id)

    def increase_balance(self, trader_id, amount):
        current = self.db.ReadTraderBalance(trader_id) or 0
        self.db.WriteTraderBalance(trader_id, current + amount)

    def decrease_balance(self, trader_id, amount):
        current = self.db.ReadTraderBalance(trader_id) or 0
        self.db.WriteTraderBalance(trader_id, current - amount)

    def increase_inventory(self, trader_id, volume):
        inv = self.db.ReadTraderInventory(trader_id) or 0
        self.db.WriteTraderInventory(trader_id, inv + volume)

    def decrease_inventory(self, trader_id, volume):
        inv = self.db.ReadTraderInventory(trader_id) or 0
        self.db.WriteTraderInventory(trader_id, inv - volume)
