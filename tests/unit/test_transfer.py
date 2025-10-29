from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfer:
    # tests for outgoing transfers
    def test_outgoing_transfer_reduces_balance(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 100.0
        account.outgoing_transfer(20.0)
        assert account.balance == 80.0

    def test_outgoing_transfer_with_sufficient_funds(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 50.0
        account.outgoing_transfer(30.0)
        assert account.balance == 20.0

    def test_outgoing_transfer_exceeding_balance(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 30.0
        account.outgoing_transfer(50.0)
        assert account.balance == 30.0 

    def test_outgoing_transfer_negative_amount(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 100.0
        account.outgoing_transfer(-20.0)
        assert account.balance == 100.0

    # tests for incoming transfers
    def test_incoming_transfer_increases_balance(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 50.0
        account.incoming_transfer(30.0)
        assert account.balance == 80.0

    def test_incoming_transfer_negative_amount(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 100.0
        account.incoming_transfer(-20.0)
        assert account.balance == 100.0  

    # tests for outgoing express transfers
    # personal
    def test_outgoing_express_transfer_with_sufficient_funds(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 100.0
        account.outgoing_express_transfer(50.0)
        assert account.balance == 49.0
    
    def test_outgoing_express_transfer_exceeding_balance(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 40.0
        account.outgoing_express_transfer(40.0)
        assert account.balance == -1.00
    
    def test_outgoing_express_transfer_negative_amount(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        account.balance = 100.0
        account.outgoing_express_transfer(-20.0)
        assert account.balance == 100.0

    # company
    def test_outgoing_express_transfer_sufficient_balance(self):
        account = CompanyAccount("TechComp", "1234567890")
        account.balance = 200.0
        account.outgoing_express_transfer(100.0)
        assert account.balance == 95.0

    def test_outgoing_express_transfer_exceeding_balance(self):
        account = CompanyAccount("TechComp", "0987654321")
        account.balance = 200.0
        account.outgoing_express_transfer(200.0)
        assert account.balance == -5.0
    
    def test_outgoing_express_transfer_negative_amount(self):
        account = CompanyAccount("TechComp", "1234567890")
        account.balance = 100.0
        account.outgoing_express_transfer(-20.0)
        assert account.balance == 100.0
    

