from src.personal_account import Account

class TestTransfer:
    # tests for outgoing transfers
    def test_outgoing_transfer_reduces_balance(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 100.0
        account.outgoing_transfer(20.0)
        assert account.balance == 80.0

    def test_outgoing_transfer_with_sufficient_funds(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 50.0
        account.outgoing_transfer(30.0)
        assert account.balance == 20.0

    def test_outgoing_transfer_exceeding_balance(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 30.0
        account.outgoing_transfer(50.0)
        assert account.balance == 30.0 

    def test_outgoing_transfer_negative_amount(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 100.0
        account.outgoing_transfer(-20.0)
        assert account.balance == 100.0

    # tests for incoming transfers
    def test_incoming_transfer_increases_balance(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 50.0
        account.incoming_transfer(30.0)
        assert account.balance == 80.0

    def test_incoming_transfer_negative_amount(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 100.0
        account.incoming_transfer(-20.0)
        assert account.balance == 100.0  
