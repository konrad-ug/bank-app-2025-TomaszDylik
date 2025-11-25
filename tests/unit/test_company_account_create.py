import pytest
from src.company_account import CompanyAccount

class TestCompanyAccountCreation:
    
    def test_create_company_account_valid(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        assert company_account.name == "Tech Solutions"
        assert company_account.nip == "1234567890"
        assert company_account.balance == 0.0
    
    @pytest.mark.parametrize("nip,expected_nip", [
        # Invalid NIPs
        ("12345", "Invalid"),  # too short
        ("123451234512345", "Invalid"),  # too long
        ("12345ABCDE", "Invalid"),  # contains non-digits
        # Valid NIP
        ("0987654321", "0987654321"),
    ])
    def test_nip_validation(self, nip, expected_nip):
        company_account = CompanyAccount("Tech Solutions", nip)
        assert company_account.nip == expected_nip