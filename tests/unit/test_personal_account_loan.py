import pytest
from src.personal_account import PersonalAccount


@pytest.fixture
def personal_account():
    return PersonalAccount("Jan", "Kowalski", "12345678901")

class TestPersonalAccountLoan:
    @pytest.mark.parametrize("transfers,loan_amount,expected_approved,expected_balance", [
        # Success cases - last 3 positive
        (
            [("incoming", 300.0), ("incoming", 400.0), ("incoming", 500.0)],
            600.0,
            True,
            1800.0
        ),
        # Success cases - last 5 sum > amount (last 3 not all positive)
        (
            [("incoming", 500.0), ("incoming", 600.0), ("incoming", 300.0), 
             ("outgoing", 100.0), ("incoming", 200.0)],
            800.0,
            True,
            2300.0
        ),
        # Failure cases - insufficient history (less than 3)
        (
            [("incoming", 100.0), ("outgoing", 50.0)],
            500.0,
            False,
            50.0
        ),
        # Failure cases - last 3 not all positive
        (
            [("incoming", 150.0), ("outgoing", 100.0), ("incoming", 200.0)],
            500.0,
            False,
            250.0
        ),
        # Failure cases - last 5 sum <= amount
        (
            [("incoming", 100.0), ("incoming", 150.0), ("outgoing", 50.0), 
             ("incoming", 200.0), ("incoming", 250.0)],
            1000.0,
            False,
            650.0
        ),
    ])
    def test_loan_scenarios(self, personal_account, transfers, loan_amount, 
                           expected_approved, expected_balance):
        # Setup: execute all transfers
        for transfer_type, amount in transfers:
            if transfer_type == "incoming":
                personal_account.incoming_transfer(amount)
            elif transfer_type == "outgoing":
                personal_account.outgoing_transfer(amount)
        
        # Act: submit loan request
        result = personal_account.submit_for_loan(loan_amount)
        
        # Assert: check result and balance
        assert result == expected_approved
        assert personal_account.balance == expected_balance
    
