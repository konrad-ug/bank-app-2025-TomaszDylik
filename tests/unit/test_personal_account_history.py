import pytest

class TestAccountHistoryInitialization:
    
    @pytest.mark.parametrize("check_method,expected", [
        ("list", []),
        ("length", 0),
    ])
    def test_account_history_initialization(self, base_account, check_method, expected):
        if check_method == "list":
            assert base_account.history == expected
        elif check_method == "length":
            assert len(base_account.history) == expected

class TestPersonalAccountHistory:
    
    @pytest.mark.parametrize("operations,expected_history", [
        # Single incoming transfer
        ([("incoming", 100.0)], [100.00]),
        # Single outgoing transfer (with initial balance)
        ([("set_balance", 100.0), ("outgoing", 50.0)], [-50.00]),
        # Outgoing transfer - insufficient funds (not added)
        ([("set_balance", 10.0), ("outgoing", 50.0)], []),
        # Incoming transfer - negative amount (not added)
        ([("incoming", -50.0)], []),
        # Express transfer with fee
        ([("set_balance", 500.0), ("express", 300.0)], [-300.00, -1.0]),
        # Express transfer - insufficient funds (not added)
        ([("set_balance", 100.0), ("express", 300.0)], []),
        # Multiple operations
        ([("incoming", 500.0), ("express", 300.0)], [500.00, -300.00, -1.0]),
        # Complex sequence
        ([("incoming", 1000.0), ("outgoing", 200.0), ("incoming", 150.0), ("express", 100.0)], 
         [1000.00, -200.00, 150.00, -100.00, -1.0]),
    ])
    def test_history_tracking(self, personal_account, operations, expected_history):
        for operation_type, amount in operations:
            if operation_type == "incoming":
                personal_account.incoming_transfer(amount)
            elif operation_type == "outgoing":
                personal_account.outgoing_transfer(amount)
            elif operation_type == "express":
                personal_account.outgoing_express_transfer(amount)
            elif operation_type == "set_balance":
                personal_account.balance = amount
        
        assert personal_account.history == expected_history