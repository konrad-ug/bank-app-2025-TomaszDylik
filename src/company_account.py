import os
from datetime import datetime
import requests
from smtp.smtp import SMTPClient
from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__()
        self.name = name
        
        # Walidacja formatu NIPu
        if not self.is_nip_valid(nip):
            self.nip = "Invalid"
        else:
            # Jeżeli format jest OK, sprawdź w bazie MF
            if not self.validate_nip_in_mf(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip
        
        self.balance = 0.0
        
    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            return True
        return False
    
    def validate_nip_in_mf(self, nip):
        """
        Waliduje NIP w bazie Ministerstwa Finansów.
        Zwraca True jeżeli NIP jest zarejestrowany i ma status "Czynny",
        False w przeciwnym wypadku.
        """
        # Pobierz URL z zmiennej środowiskowej, domyślnie testowe API
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        
        # Pobierz dzisiejszą datę w formacie YYYY-MM-DD
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Zbuduj pełny URL
        url = f"{base_url}/api/search/nip/{nip}?date={today}"
        
        try:
            # Wyślij zapytanie do API
            response = requests.get(url, timeout=10)
            
            # Wypisz odpowiedź w logach
            print(f"MF API Response for NIP {nip}:")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Sprawdź czy request się powiódł
            if response.status_code == 200:
                data = response.json()
                
                # Sprawdź czy w odpowiedzi jest statusVat: "Czynny"
                if "result" in data and "subject" in data["result"]:
                    subject = data["result"]["subject"]
                    # subject może być null jeżeli NIP nie istnieje
                    if subject is not None:
                        status_vat = subject.get("statusVat")
                        return status_vat == "Czynny"
            
            return False
            
        except Exception as e:
            print(f"Error during NIP validation: {e}")
            return False
    
    def outgoing_express_transfer(self, amount: float) -> bool:
        fee = 5.0
        return super().outgoing_express_transfer(amount, fee)
    
    def take_loan(self, amount: float) -> bool:

        # Check if balance is sufficient
        if self.balance < amount * 2:
            return False
        
        # Check ZUS payment in history (-1775.0)
        has_zus_payment = -1775.0 in self.history
        
        if has_zus_payment:
            self.balance += amount
            return True
        
        return False
    
    def send_history_via_email(self, email_address: str) -> bool:
        """
        Send account transfer history via email.
        
        Args:
            email_address: Recipient email address
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        # Prepare email subject with today's date
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        
        # Prepare email body
        text = f"Company account history:{self.history}"
        
        # Send email using SMTP client
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)
