import pytest
from unittest.mock import patch, Mock
from src.company_account import CompanyAccount

class TestCompanyAccountCreation:
    
    @patch('src.company_account.requests.get')
    def test_create_company_account_valid(self, mock_get):
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
        
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        assert company_account.name == "Tech Solutions"
        assert company_account.nip == "1234567890"
        assert company_account.balance == 0.0
    
    @pytest.mark.parametrize("nip,expected_nip", [
        # Invalid NIPs - nie wysyłają requestu
        ("12345", "Invalid"),  # too short
        ("123451234512345", "Invalid"),  # too long
        ("12345ABCDE", "Invalid"),  # contains non-digits
    ])
    def test_nip_validation(self, nip, expected_nip):
        company_account = CompanyAccount("Tech Solutions", nip)
        assert company_account.nip == expected_nip
    
    @patch('src.company_account.requests.get')
    def test_valid_format_nip(self, mock_get):
        # Mock odpowiedzi API dla poprawnego NIPu
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
        
        company_account = CompanyAccount("Tech Solutions", "0987654321")
        assert company_account.nip == "0987654321"