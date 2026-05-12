class CurrencyManager:
    def __init__(self):
        self.bronze = 0
        self.silver = 0
        self.gold = 0

    def add_bronze(self, amount):
        self.bronze += amount
        self._convert()

    def _convert(self):
        # 100 Bronze = 1 Silver
        if self.bronze >= 100:
            self.silver += self.bronze // 100
            self.bronze %= 100
        # 100 Silver = 1 Gold
        if self.silver >= 100:
            self.gold += self.silver // 100
            self.silver %= 100
