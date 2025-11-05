from src.company_account import CompanyAccount


class TestCompanyAccountHistory:
    def test_company_account_initialization_history_empty(self):
        account = CompanyAccount("TechCorp", "1234567890")
        assert account.history == []
    
    def test_company_account_history_initially_empty(self):
        account = CompanyAccount("TechCorp", "1234567890")
        assert len(account.history) == 0

    def test_incoming_transfer_adds_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(1000.0)
        assert account.history == [1000.00]

    def test_outgoing_transfer_adds_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.balance = 500.0
        account.outgoing_transfer(200.0)
        assert account.history == [-200.00]
    
    def test_outgoing_transfer_insufficient_funds_not_added_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.balance = 50.0
        account.outgoing_transfer(200.0)
        assert account.history == []
    
    def test_incoming_transfer_negative_amount_not_added_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(-100.0)
        assert account.history == []
    
    def test_outgoing_express_transfer_adds_amount_and_fee_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.balance = 1000.0
        account.outgoing_express_transfer(500.0)
        assert account.history == [-500.00, -5.0]
    
    def test_outgoing_express_transfer_insufficient_funds_not_added_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.balance = 100.0
        account.outgoing_express_transfer(500.0)
        assert account.history == []
    
    def test_multiple_operations_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(2000.0)
        account.outgoing_express_transfer(800.0)
        assert account.history == [2000.00, -800.00, -5.0]
    
    def test_complex_history_sequence(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(5000.0)
        account.outgoing_transfer(1000.0)
        account.incoming_transfer(500.0)
        account.outgoing_express_transfer(300.0)
        account.outgoing_transfer(100.0)
        assert account.history == [5000.00, -1000.00, 500.00, -300.00, -5.0, -100.00]
    
    def test_outgoing_transfer_zero_amount_not_added_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.balance = 1000.0
        account.outgoing_transfer(0.0)
        assert account.history == []
    
    def test_incoming_transfer_zero_amount_not_added_to_history(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(0.0)
        assert account.history == []
