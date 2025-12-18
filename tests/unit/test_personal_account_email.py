import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.personal_account import PersonalAccount


class TestPersonalAccountEmailHistory:
    """Testy wysyłania historii konta osobistego na email"""
    
    @patch('src.personal_account.SMTPClient')
    @patch('src.personal_account.datetime')
    def test_send_history_via_email_success(self, mock_datetime, mock_smtp_class):
        """Test: Pomyślne wysłanie emaila z historią konta"""
        # Mock daty - używamy konkretnej daty dla strftime
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-15"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto i dodaj historię
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.history = [150.0, -50.0]
        
        # Wyślij historię
        result = account.send_history_via_email("test@email.com")
        
        # Sprawdzenia
        assert result is True
        mock_smtp_instance.send.assert_called_once()
        
        # Sprawdź parametry wywołania
        call_args = mock_smtp_instance.send.call_args[0]
        subject = call_args[0]
        text = call_args[1]
        email = call_args[2]
        
        assert subject == "Account Transfer History 2025-12-15"
        assert text == "Personal account history:[150.0, -50.0]"
        assert email == "test@email.com"
    
    @patch('src.personal_account.SMTPClient')
    @patch('src.personal_account.datetime')
    def test_send_history_via_email_failure(self, mock_datetime, mock_smtp_class):
        """Test: Nieudane wysłanie emaila (SMTP zwraca False)"""
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-15"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client - zwraca False
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.history = [100.0, -25.0, 300.0]
        
        # Wyślij historię
        result = account.send_history_via_email("test@email.com")
        
        # Sprawdzenia
        assert result is False
        mock_smtp_instance.send.assert_called_once()
    
    @patch('src.personal_account.SMTPClient')
    @patch('src.personal_account.datetime')
    def test_send_history_via_email_empty_history(self, mock_datetime, mock_smtp_class):
        """Test: Wysłanie emaila z pustą historią"""
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-18"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto z pustą historią
        account = PersonalAccount("Anna", "Nowak", "98765432109")
        
        # Wyślij historię
        result = account.send_history_via_email("anna@example.com")
        
        # Sprawdzenia
        assert result is True
        call_args = mock_smtp_instance.send.call_args[0]
        text = call_args[1]
        assert text == "Personal account history:[]"
    
    @patch('src.personal_account.SMTPClient')
    @patch('src.personal_account.datetime')
    def test_send_history_via_email_with_transfers(self, mock_datetime, mock_smtp_class):
        """Test: Wysłanie emaila po wykonaniu transferów"""
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-11-30"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto i wykonaj operacje
        account = PersonalAccount("Piotr", "Wiśniewski", "55555555555")
        account.balance = 1000.0
        account.incoming_transfer(500.0)
        account.outgoing_transfer(200.0)
        
        # Wyślij historię
        result = account.send_history_via_email("piotr@test.com")
        
        # Sprawdzenia
        assert result is True
        call_args = mock_smtp_instance.send.call_args[0]
        text = call_args[1]
        assert "500.0" in text
        assert "-200.0" in text
    
    @patch('src.personal_account.SMTPClient')
    @patch('src.personal_account.datetime')
    def test_send_history_called_with_correct_parameters(self, mock_datetime, mock_smtp_class):
        """Test: Sprawdzenie czy metoda send została wywołana z poprawnymi parametrami"""
        # Mock daty
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-12-10"
        mock_datetime.now.return_value = mock_now
        
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Utwórz konto
        account = PersonalAccount("Test", "User", "11111111111")
        account.history = [100.0, -50.0, 200.0]
        
        # Wyślij historię
        account.send_history_via_email("recipient@example.com")
        
        # Sprawdź czy metoda została wywołana dokładnie raz
        mock_smtp_instance.send.assert_called_once_with(
            "Account Transfer History 2025-12-10",
            "Personal account history:[100.0, -50.0, 200.0]",
            "recipient@example.com"
        )
    
    @patch('src.personal_account.SMTPClient')
    @patch('src.personal_account.datetime')
    def test_send_history_different_dates(self, mock_datetime, mock_smtp_class):
        """Test: Wysłanie emaila w różnych datach"""
        # Mock SMTP client
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        
        # Test z różnymi datami
        test_dates = [
            "2025-01-01",
            "2025-06-15",
            "2025-12-31",
        ]
        
        for date_str in test_dates:
            mock_now = Mock()
            mock_now.strftime.return_value = date_str
            mock_datetime.now.return_value = mock_now
            
            result = account.send_history_via_email("test@email.com")
            
            assert result is True
            call_args = mock_smtp_instance.send.call_args[0]
            subject = call_args[0]
            assert subject == f"Account Transfer History {date_str}"
