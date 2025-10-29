from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_create_company_account(self):
        company_account = CompanyAccount("Tech Solutions", "1234567890")
        assert company_account.name == "Tech Solutions"
        assert company_account.nip == "1234567890"
        assert company_account.balance == 0.0
    
    # inavlid NIP tests
    def test_invalid_nip_too_short(self):
        company_account = CompanyAccount("Tech Solutions", "12345")
        assert company_account.nip == "Invalid"
    
    def test_invalid_nip_too_long(self):
        company_account = CompanyAccount("Tech Solutions", "123451234512345")
        assert company_account.nip == "Invalid"

    def test_invalid_nip_non_digit(self):
        company_account = CompanyAccount("Tech Solutions", "12345ABCDE")
        assert company_account.nip == "Invalid"
    
    # valid NIp tests
    def test_valid_nip(self):
        company_account = CompanyAccount("Tech Solutions", "0987654321")
        assert company_account.nip == "0987654321"