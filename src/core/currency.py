class CurrencyManager:
    def __init__(self):
        self.bronze = 0
        self.silver = 0
        self.gold = 0

    def add_bronze(self, amount):
        self.bronze += amount
        self._convert()

    def get_total_bronze(self):
        return self.bronze + (self.silver * 100) + (self.gold * 10000)

    def deduct_bronze(self, amount):
        total = self.get_total_bronze()
        if total >= amount:
            remaining = total - amount
            self.gold = remaining // 10000
            remaining %= 10000
            self.silver = remaining // 100
            self.bronze = remaining % 100
            return True
        return False

    def _convert(self):
        # 100 Bronze = 1 Silver
        if self.bronze >= 100:
            self.silver += self.bronze // 100
            self.bronze %= 100
        # 100 Silver = 1 Gold
        if self.silver >= 100:
            self.gold += self.silver // 100
            self.silver %= 100
