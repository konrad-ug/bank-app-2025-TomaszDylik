import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.company_account import CompanyAccount


class TestCompanyAccountEmailHistory:
    """Testy wysyłania historii konta firmowego na email"""
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    @patch('src.company_account.datetime')
    def test_send_history_via_email_success(self, mock_datetime, mock_smtp_class, mock_get):
        """Test: Pomyślne wysłanie emaila z historią konta firmowego"""
        # Mock API MF (dla walidacji NIPu)
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
        
        # Mock daty - używamy konkretnej daty dla strftime
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-15"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto i dodaj historię
        account = CompanyAccount("Tech Corp", "1234567890")
        account.history = [5000.0, -1000.0, 500.0]
        
        # Wyślij historię
        result = account.send_history_via_email("company@email.com")
        
        # Sprawdzenia
        assert result is True
        mock_smtp_instance.send.assert_called_once()
        
        # Sprawdź parametry wywołania
        call_args = mock_smtp_instance.send.call_args[0]
        subject = call_args[0]
        text = call_args[1]
        email = call_args[2]
        
        assert subject == "Account Transfer History 2025-12-15"
        assert text == "Company account history:[5000.0, -1000.0, 500.0]"
        assert email == "company@email.com"
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    @patch('src.company_account.datetime')
    def test_send_history_via_email_failure(self, mock_datetime, mock_smtp_class, mock_get):
        """Test: Nieudane wysłanie emaila (SMTP zwraca False)"""
        # Mock API MF
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
        
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-15"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client - zwraca False
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto
        account = CompanyAccount("Failed Corp", "9876543210")
        account.history = [1000.0, -500.0]
        
        # Wyślij historię
        result = account.send_history_via_email("fail@email.com")
        
        # Sprawdzenia
        assert result is False
        mock_smtp_instance.send.assert_called_once()
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    @patch('src.company_account.datetime')
    def test_send_history_via_email_empty_history(self, mock_datetime, mock_smtp_class, mock_get):
        """Test: Wysłanie emaila z pustą historią"""
        # Mock API MF
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
        
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-18"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto z pustą historią
        account = CompanyAccount("Empty Corp", "1111111111")
        
        # Wyślij historię
        result = account.send_history_via_email("empty@example.com")
        
        # Sprawdzenia
        assert result is True
        call_args = mock_smtp_instance.send.call_args[0]
        text = call_args[1]
        assert text == "Company account history:[]"
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    @patch('src.company_account.datetime')
    def test_send_history_called_with_correct_parameters(self, mock_datetime, mock_smtp_class, mock_get):
        """Test: Sprawdzenie czy metoda send została wywołana z poprawnymi parametrami"""
        # Mock API MF
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
        
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-10"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto
        account = CompanyAccount("Test Company", "2222222222")
        account.history = [10000.0, -2000.0, 3000.0]
        
        # Wyślij historię
        account.send_history_via_email("company@example.com")
        
        # Sprawdź czy metoda została wywołana dokładnie raz z poprawnymi parametrami
        mock_smtp_instance.send.assert_called_once_with(
            "Account Transfer History 2025-12-10",
            "Company account history:[10000.0, -2000.0, 3000.0]",
            "company@example.com"
        )
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    @patch('src.company_account.datetime')
    def test_send_history_with_zus_payment(self, mock_datetime, mock_smtp_class, mock_get):
        """Test: Wysłanie emaila z historią zawierającą płatność ZUS"""
        # Mock API MF
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
        
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-01"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto z płatnością ZUS
        account = CompanyAccount("ZUS Corp", "3333333333")
        account.history = [10000.0, -1775.0, 5000.0]  # -1775.0 to płatność ZUS
        
        # Wyślij historię
        result = account.send_history_via_email("zus@company.com")
        
        # Sprawdzenia
        assert result is True
        call_args = mock_smtp_instance.send.call_args[0]
        text = call_args[1]
        assert "-1775.0" in text
    
    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    @patch('src.company_account.datetime')
    def test_send_history_different_email_addresses(self, mock_datetime, mock_smtp_class, mock_get):
        """Test: Wysłanie historii na różne adresy email"""
        # Mock API MF
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
        
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-15"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto
        account = CompanyAccount("Multi Email Corp", "4444444444")
        account.history = [1000.0, -100.0]
        
        # Test z różnymi adresami email
        test_emails = [
            "ceo@company.com",
            "accountant@company.com",
            "auditor@company.com",
        ]
        
        for email in test_emails:
            result = account.send_history_via_email(email)
            assert result is True
            
            # Sprawdź czy email został wysłany na poprawny adres
            call_args = mock_smtp_instance.send.call_args[0]
            assert call_args[2] == email
