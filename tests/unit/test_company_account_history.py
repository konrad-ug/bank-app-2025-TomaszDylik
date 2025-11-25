import pytest

class TestCompanyAccountHistory:
    
    @pytest.mark.parametrize("check_method,expected", [
        ("list", []),
        ("length", 0),
    ])
    def test_company_account_initialization(self, company_account, check_method, expected):
        if check_method == "list":
            assert company_account.history == expected
        elif check_method == "length":
            assert len(company_account.history) == expected

    @pytest.mark.parametrize("operations,expected_history", [
        # Single incoming transfer
        ([("incoming", 1000.0)], [1000.00]),
        # Single outgoing transfer (with initial balance)
        ([("set_balance", 500.0), ("outgoing", 200.0)], [-200.00]),
        # Outgoing transfer - insufficient funds (not added)
        ([("set_balance", 50.0), ("outgoing", 200.0)], []),
        # Incoming transfer - negative amount (not added)
        ([("incoming", -100.0)], []),
        # Incoming transfer - zero amount (not added)
        ([("incoming", 0.0)], []),
        # Outgoing transfer - zero amount (not added)
        ([("set_balance", 1000.0), ("outgoing", 0.0)], []),
        # Express transfer with fee
        ([("set_balance", 1000.0), ("express", 500.0)], [-500.00, -5.0]),
        # Express transfer - insufficient funds (not added)
        ([("set_balance", 100.0), ("express", 500.0)], []),
        # Multiple operations
        ([("incoming", 2000.0), ("express", 800.0)], [2000.00, -800.00, -5.0]),
        # Complex sequence
        ([("incoming", 5000.0), ("outgoing", 1000.0), ("incoming", 500.0), 
          ("express", 300.0), ("outgoing", 100.0)], 
         [5000.00, -1000.00, 500.00, -300.00, -5.0, -100.00]),
    ])
    def test_history_tracking(self, company_account, operations, expected_history):
        for operation_type, amount in operations:
            if operation_type == "incoming":
                company_account.incoming_transfer(amount)
            elif operation_type == "outgoing":
                company_account.outgoing_transfer(amount)
            elif operation_type == "express":
                company_account.outgoing_express_transfer(amount)
            elif operation_type == "set_balance":
                company_account.balance = amount
        
        assert company_account.history == expected_history
