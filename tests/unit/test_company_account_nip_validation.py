import pytest
from unittest.mock import patch, Mock
from src.company_account import CompanyAccount


class TestCompanyAccountNipValidation:
    
    @patch('src.company_account.requests.get')
    def test_valid_nip_active_company(self, mock_get):
        """Test tworzenia konta z poprawnym, aktywnym NIPem"""
        # Mock odpowiedzi API z statusem "Czynny"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny",
                    "name": "Test Company"
                }
            }
        }
        mock_get.return_value = mock_response
        
        # Powinno się udać utworzyć konto
        company_account = CompanyAccount("Tech Solutions", "8461627563")
        assert company_account.name == "Tech Solutions"
        assert company_account.nip == "8461627563"
        assert company_account.balance == 0.0
    
    @patch('src.company_account.requests.get')
    def test_valid_nip_inactive_company(self, mock_get):
        """Test tworzenia konta z NIPem o statusie innym niż Czynny"""
        # Mock odpowiedzi API z statusem "Zwolniony"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"result": {"subject": {"statusVat": "Zwolniony"}}}'
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Zwolniony"
                }
            }
        }
        mock_get.return_value = mock_response
        
        # Powinno rzucić ValueError
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Tech Solutions", "1234567890")
    
    @patch('src.company_account.requests.get')
    def test_nip_not_found_in_database(self, mock_get):
        """Test tworzenia konta z NIPem nieistniejącym w bazie MF"""
        # Mock odpowiedzi API - 404 Not Found
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = '{"message": "Not found"}'
        mock_get.return_value = mock_response
        
        # Powinno rzucić ValueError
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Tech Solutions", "9999999999")
    
    @patch('src.company_account.requests.get')
    def test_api_timeout(self, mock_get):
        """Test obsługi błędu timeout przy zapytaniu do API"""
        # Mock timeout exception
        mock_get.side_effect = Exception("Connection timeout")
        
        # Powinno rzucić ValueError gdy API nie odpowiada
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Tech Solutions", "1234567890")
    
    def test_invalid_nip_too_short(self):
        """Test z NIPem zbyt krótkim - nie wysyła requestu"""
        # Nie powinno rzucić ValueError, tylko ustawić nip na "Invalid"
        company_account = CompanyAccount("Tech Solutions", "12345")
        assert company_account.nip == "Invalid"
    
    def test_invalid_nip_too_long(self):
        """Test z NIPem zbyt długim - nie wysyła requestu"""
        company_account = CompanyAccount("Tech Solutions", "123456789012")
        assert company_account.nip == "Invalid"
    
    def test_invalid_nip_contains_letters(self):
        """Test z NIPem zawierającym litery - nie wysyła requestu"""
        company_account = CompanyAccount("Tech Solutions", "12345ABCDE")
        assert company_account.nip == "Invalid"
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.os.getenv')
    def test_uses_env_variable_for_url(self, mock_getenv, mock_get):
        """Test czy używa zmiennej środowiskowej BANK_APP_MF_URL"""
        # Mock zmiennej środowiskowej
        mock_getenv.return_value = "https://custom-api.example.com"
        
        # Mock odpowiedzi API
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
        
        CompanyAccount("Tech Solutions", "8461627563")
        
        # Sprawdź czy getenv został wywołany z odpowiednim kluczem
        mock_getenv.assert_called_with("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        
        # Sprawdź czy request został wysłany na poprawny URL
        called_url = mock_get.call_args[0][0]
        assert called_url.startswith("https://custom-api.example.com")
    
    @patch('src.company_account.requests.get')
    def test_default_url_when_env_not_set(self, mock_get):
        """Test czy używa domyślnego URL testowego gdy brak zmiennej środowiskowej"""
        # Mock odpowiedzi API
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
        
        CompanyAccount("Tech Solutions", "8461627563")
        
        # Sprawdź czy request został wysłany na domyślny URL testowy
        called_url = mock_get.call_args[0][0]
        assert called_url.startswith("https://wl-test.mf.gov.pl")
    
    @patch('src.company_account.requests.get')
    def test_response_without_subject(self, mock_get):
        """Test obsługi odpowiedzi API bez pola subject"""
        # Mock odpowiedzi API bez subject
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"result": {}}'
        mock_response.json.return_value = {
            "result": {}
        }
        mock_get.return_value = mock_response
        
        # Powinno rzucić ValueError
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Tech Solutions", "1234567890")


class TestCompanyAccountConstructorExceptions:
    """Dodatkowe testy sprawdzające rzucanie wyjątków przez konstruktor"""
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_for_nonexistent_nip(self, mock_get):
        """Test: Konstruktor rzuca ValueError gdy NIP nie istnieje w bazie MF"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = '{"message": "NIP not found"}'
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            CompanyAccount("Nonexistent Corp", "1234567890")
        
        assert str(exc_info.value) == "Company not registered!!"
        assert exc_info.type == ValueError
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_for_status_zwolniony(self, mock_get):
        """Test: Konstruktor rzuca ValueError dla statusu 'Zwolniony'"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Zwolniony"
                }
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            CompanyAccount("Inactive Company", "9876543210")
        
        assert "Company not registered!!" in str(exc_info.value)
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_for_status_nieczynny(self, mock_get):
        """Test: Konstruktor rzuca ValueError dla statusu 'Nieczynny'"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Nieczynny"
                }
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Inactive Company", "5555555555")
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_when_api_returns_500(self, mock_get):
        """Test: Konstruktor rzuca ValueError gdy API zwraca błąd 500"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = '{"error": "Internal server error"}'
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Error Company", "1111111111")
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_when_subject_is_null(self, mock_get):
        """Test: Konstruktor rzuca ValueError gdy subject jest null"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": None
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Null Company", "2222222222")
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_on_network_error(self, mock_get):
        """Test: Konstruktor rzuca ValueError przy błędzie sieci"""
        mock_get.side_effect = ConnectionError("Network unreachable")
        
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Network Error Corp", "3333333333")
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_on_timeout_error(self, mock_get):
        """Test: Konstruktor rzuca ValueError przy timeout"""
        import requests
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Timeout Corp", "4444444444")
    
    @patch('src.company_account.requests.get')
    def test_constructor_raises_valueerror_on_json_decode_error(self, mock_get):
        """Test: Konstruktor rzuca ValueError przy błędzie parsowania JSON"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Bad JSON Corp", "6666666666")
    
    def test_constructor_does_not_raise_for_invalid_format_nip(self):
        """Test: Konstruktor NIE rzuca ValueError dla złego formatu NIPu (ustawia 'Invalid')"""
        # To NIE powinno rzucić ValueError - tylko ustawić nip = "Invalid"
        try:
            account = CompanyAccount("Bad Format", "123")
            assert account.nip == "Invalid"
        except ValueError:
            pytest.fail("Konstruktor nie powinien rzucać ValueError dla złego formatu NIPu")
    
    @patch('src.company_account.requests.get')
    def test_constructor_success_with_valid_active_nip(self, mock_get):
        """Test: Konstruktor SUKCES - nie rzuca błędu dla aktywnego NIPu"""
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
        
        # To NIE powinno rzucić ValueError
        try:
            account = CompanyAccount("Valid Active Corp", "7777777777")
            assert account.nip == "7777777777"
            assert account.name == "Valid Active Corp"
            assert account.balance == 0.0
        except ValueError:
            pytest.fail("Konstruktor nie powinien rzucać ValueError dla aktywnego NIPu")

