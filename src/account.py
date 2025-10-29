class Account:

    def incoming_transfer(self, amount: float) -> None:
        if amount > 0:     
            self.balance += amount

    def outgoing_transfer(self, amount: float) -> None:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount 

    def outgoing_express_transfer(self, amount: float, fee: float) -> bool:
        if amount > 0 and self.balance >= amount:
            self.balance -= (amount + fee)
            return True
        return False
