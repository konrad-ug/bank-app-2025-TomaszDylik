from src.company_account import CompanyAccount
import pytest

@pytest.fixture
def company_account():
    return CompanyAccount("Tech Solutions", "1234567890")

class TestCompanyAccountLoan:

    @pytest.mark.parametrize("transfers,initial_balance,loan_amount,expected_approved,expected_balance", [
        # Valid loan scenario - ZUS paid, balance > 2x loan
        ( 
            [("incoming", 500.0), ("incoming", 6000.0), ("outgoing", 1775.0)],
            275.0,
            1000.0,
            True,
            6000.0  # 5000 (after transfers) + 1000 (loan)
        ),
        # Invalid: ZUS paid but balance too low (not > 2x loan)
        (
            [("incoming", 2000.0), ("outgoing", 1775.0), ("incoming", 100.0)],
            75.0,
            1000.0,
            False,
            400.0  # balance unchanged (loan rejected)
        ),
        # Invalid: Balance sufficient but no ZUS payment
        (
            [("incoming", 5000.0), ("outgoing", 300.0), ("incoming", 200.0)],
            100.0,
            1000.0,
            False,
            5000.0  # balance unchanged (loan rejected)
        ),
        # Invalid: Balance sufficient but no ZUS payment
        (
            [("incoming", 1000.0), ("outgoing", 200.0), ("incoming", 100.0)],
            1000.0,
            1000.0,
            False,
            1900.0  # balance unchanged (loan rejected)
        ),
    ])
    def test_company_account_loan(self, company_account, transfers, initial_balance, loan_amount, 
                                  expected_approved, expected_balance):
        """Test company account loan approval based on balance and ZUS payment."""
        # Setup: execute all transfers
        company_account.balance = initial_balance
        for transfer_type, amount in transfers:
            if transfer_type == "incoming":
                company_account.incoming_transfer(amount)
            elif transfer_type == "outgoing":
                company_account.outgoing_transfer(amount)
        
        # Act: submit loan request
        result = company_account.take_loan(loan_amount)
        
        # Assert
        assert result == expected_approved
        assert company_account.balance == expected_balance