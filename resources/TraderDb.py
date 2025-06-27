# resources/TraderDb.py

class TraderDb:
    def __init__(self):
        self.traders = {}

    def CreateTrader(self, trader):
        self.traders[trader.id] = trader

    def ReadTrader(self, trader_id):
        return self.traders.get(trader_id)

    def WriteTrader(self, trader):
        self.traders[trader.id] = trader

    def ReadTraderBalance(self, trader_id):
        trader = self.ReadTrader(trader_id)
        return trader.cash if trader else None

    def WriteTraderBalance(self, trader_id, amount):
        trader = self.ReadTrader(trader_id)
        if trader:
            trader.cash = amount
            self.WriteTrader(trader)

    def ReadTraderInventory(self, trader_id):
        trader = self.ReadTrader(trader_id)
        return trader.inventory if trader else None

    def WriteTraderInventory(self, trader_id, inventory):
        trader = self.ReadTrader(trader_id)
        if trader:
            trader.inventory = inventory
            self.WriteTrader(trader)
