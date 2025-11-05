class Account:

    def __init__(self) -> None:
        self.history = []

    def incoming_transfer(self, amount: float) -> None:
        if amount > 0:     
            self.balance += amount
            self.history.append(amount)

    def outgoing_transfer(self, amount: float) -> None:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount 
            self.history.append(-amount)

    def outgoing_express_transfer(self, amount: float, fee: float) -> bool:
        if amount > 0 and self.balance >= amount:
            self.balance -= (amount + fee)
            self.history.append(-amount)
            self.history.append(-fee)
            return True
        return False
