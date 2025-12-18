from src.personal_account import PersonalAccount
class AccountRegistry:

    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)
    
    def find_account_by_pesel(self, pesel: str):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None
    
    def pesel_exists(self, pesel: str) -> bool:
        """Check if an account with given PESEL already exists in the registry."""
        return self.find_account_by_pesel(pesel) is not None
    
    def return_all_accounts(self):
        return self.accounts
    
    def length(self):
        return len(self.accounts)