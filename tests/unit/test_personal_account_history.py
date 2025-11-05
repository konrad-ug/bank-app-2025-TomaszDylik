from src.account import Account
from src.personal_account import PersonalAccount

class TestAccount:
    def test_account_initialization(self):
        account = Account()
        assert account.history == []
    
    def test_account_history_initially_empty(self):
        account = Account()
        assert len(account.history) == 0

    def test_incoming_transfer_adds_to_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(100.0)
        assert account.history == [100.00]

    def test_outgoing_transfer_adds_to_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 100.0
        account.outgoing_transfer(50.0)
        assert account.history == [-50.00]
    
    def test_outgoing_transfer_insufficient_funds_not_added_to_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 10.0
        account.outgoing_transfer(50.0)
        assert account.history == []
    
    def test_incoming_transfer_negative_amount_not_added_to_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(-50.0)
        assert account.history == []
    
    def test_outgoing_express_transfer_adds_amount_and_fee_to_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 500.0
        account.outgoing_express_transfer(300.0)
        assert account.history == [-300.00, -1.0]
    
    def test_outgoing_express_transfer_insufficient_funds_not_added_to_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 100.0
        account.outgoing_express_transfer(300.0)
        assert account.history == []
    
    def test_multiple_operations_history(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(500.0)
        account.outgoing_express_transfer(300.0)
        assert account.history == [500.00, -300.00, -1.0]
    
    def test_complex_history_sequence(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(1000.0)
        account.outgoing_transfer(200.0)
        account.incoming_transfer(150.0)
        account.outgoing_express_transfer(100.0)
        assert account.history == [1000.00, -200.00, 150.00, -100.00, -1.0]