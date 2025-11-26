from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__()
        self.name = name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0.0
        
    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            return True
        return False
    
    def outgoing_express_transfer(self, amount: float) -> bool:
        fee = 5.0
        return super().outgoing_express_transfer(amount, fee)
    
    def take_loan(self, amount: float) -> bool:

        # Check if balance is sufficient
        if self.balance < amount * 2:
            return False
        
        # Check ZUS payment in history (-1775.0)
        has_zus_payment = -1775.0 in self.history
        
        if has_zus_payment:
            self.balance += amount
            return True
        
        return False
    