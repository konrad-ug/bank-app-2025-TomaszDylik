from src.account import Account
from src.personal_account import PersonalAccount

class TestAccount:
    ## success cases
    def test_account_get_loan_successful(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(300.0)
        account.incoming_transfer(400.0)
        account.incoming_transfer(500.0)
        assert account.submit_for_loan(600.0) == True
        assert account.balance == 1800.0
    
    def test_account_get_loan_sum_last_five_over_amount(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(200.0)
        account.outgoing_transfer(100.0)
        account.incoming_transfer(300.0)
        account.incoming_transfer(400.0)
        account.incoming_transfer(500.0)
        assert account.submit_for_loan(1000.0) == True
        assert account.balance == 2300.0

    ## failure cases
    def test_account_get_loan_insufficient_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(100.0)
        account.outgoing_transfer(50.0)
        assert account.submit_for_loan(500.0) == False
        assert account.balance == 50.0

    def test_account_get_loan_negative_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(150.0)
        account.outgoing_transfer(100.0)
        account.incoming_transfer(200.0)
        assert account.submit_for_loan(500.0) == False
        assert account.balance == 250.0
    
    def test_account_get_loan_sum_last_five_below_amount(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(100.0)
        account.incoming_transfer(150.0)
        account.outgoing_transfer(50.0)
        account.incoming_transfer(200.0)
        account.incoming_transfer(250.0)
        assert account.submit_for_loan(1000.0) == False
        assert account.balance == 650.0
    
