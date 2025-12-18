import pytest
from unittest.mock import patch, Mock
from src.company_account import CompanyAccount

class TestPersonalAccountTransfers:
    
    @pytest.mark.parametrize("initial_balance,transfer_amount,expected_balance", [
        # Outgoing transfers - valid scenarios
        (100.0, 20.0, 80.0),
        (50.0, 30.0, 20.0),
        # Outgoing transfer - exceeding balance (should not change)
        (30.0, 50.0, 30.0),
        # Outgoing transfer - negative amount (should not change)
        (100.0, -20.0, 100.0),
    ])
    def test_outgoing_transfer(self, personal_account_john, initial_balance, 
                               transfer_amount, expected_balance):
        personal_account_john.balance = initial_balance
        personal_account_john.outgoing_transfer(transfer_amount)
        assert personal_account_john.balance == expected_balance

    @pytest.mark.parametrize("initial_balance,transfer_amount,expected_balance", [
        # Incoming transfer - valid
        (50.0, 30.0, 80.0),
        # Incoming transfer - negative amount (should not change)
        (100.0, -20.0, 100.0),
    ])
    def test_incoming_transfer(self, personal_account_john, initial_balance, 
                               transfer_amount, expected_balance):
        personal_account_john.balance = initial_balance
        personal_account_john.incoming_transfer(transfer_amount)
        assert personal_account_john.balance == expected_balance

    @pytest.mark.parametrize("initial_balance,transfer_amount,expected_balance", [
        # Express transfer - sufficient funds
        (100.0, 50.0, 49.0),
        # Express transfer - exactly at balance (goes negative due to fee)
        (40.0, 40.0, -1.0),
        # Express transfer - negative amount (should not change)
        (100.0, -20.0, 100.0),
    ])
    def test_outgoing_express_transfer(self, personal_account_john, initial_balance, 
                                       transfer_amount, expected_balance):
        personal_account_john.balance = initial_balance
        personal_account_john.outgoing_express_transfer(transfer_amount)
        assert personal_account_john.balance == expected_balance


class TestCompanyAccountTransfers:
    
    @pytest.mark.parametrize("initial_balance,transfer_amount,expected_balance,nip", [
        # Express transfer - sufficient balance
        (200.0, 100.0, 95.0, "1234567890"),
        # Express transfer - exactly at balance (goes negative due to fee)
        (200.0, 200.0, -5.0, "0987654321"),
        # Express transfer - negative amount (should not change)
        (100.0, -20.0, 100.0, "1234567890"),
    ])
    @patch('src.company_account.requests.get')
    def test_outgoing_express_transfer(self, mock_get, initial_balance, transfer_amount, 
                                       expected_balance, nip):
        # Mock odpowiedzi API z statusem "Czynny"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny"
                }
            }
        }
        mock_get.return_value = mock_response
        
        account = CompanyAccount("TechComp", nip)
        account.balance = initial_balance
        account.outgoing_express_transfer(transfer_amount)
        assert account.balance == expected_balance
    

