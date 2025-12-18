"""Global pytest fixtures for all test modules."""
import pytest
from unittest.mock import patch, Mock
from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


@pytest.fixture
def base_account():
    return Account()


@pytest.fixture
def personal_account():
    return PersonalAccount("Jan", "Kowalski", "12345678901")


@pytest.fixture
def personal_account_john():
    return PersonalAccount("John", "Doe", "12345678910")


@pytest.fixture
def company_account():
    # Mock API response dla fixture
    with patch('src.company_account.requests.get') as mock_get:
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
        return CompanyAccount("TechCorp", "1234567890")
