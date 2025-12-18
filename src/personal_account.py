from datetime import datetime
from smtp.smtp import SMTPClient
from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None, younger_than_60=True):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Inavlid"
        self.promo_code = promo_code
        self.younger_than_60 = self.is_eligible_for_promotion()
        if self.is_promo_code_valid(promo_code) and self.younger_than_60:
            self.balance += 50.0
    
    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        return False

    def is_promo_code_valid(self, promo_code):
        if promo_code is None or promo_code == "":
            return False
        
        if not isinstance(promo_code, str):
            return False
        
        if promo_code.startswith("PROM_") and len(promo_code) > 5:
            return True        
        
        return False
    
    def is_eligible_for_promotion(self):
        if self.pesel == "Inavlid":
            return False
        
        year_prefix = int(self.pesel[0:2])
        month = int(self.pesel[2:4])
        # XXI century
        if month >= 20:
            return True
        
        if year_prefix > 65:
            return True
        
        return False
    
    def outgoing_express_transfer(self, amount: float) -> bool:
        fee = 1.0
        return super().outgoing_express_transfer(amount, fee)

    def _has_last_three_positive(self) -> bool:
        if len(self.history) < 3:
            return False
        last_three = self.history[-3:]
        return all(entry > 0 for entry in last_three)
    
    def _sum_last_five_exceeds(self, amount: float) -> bool:
        if len(self.history) < 5:
            return False
        last_five = self.history[-5:]
        total = sum(last_five)
        return total > amount

    def submit_for_loan(self, amount: float) -> bool:
        # Check criterion 1: last 3 positive
        if self._has_last_three_positive():
            self.balance += amount
            return True
        
        # Check criterion 2: sum of last 5 exceeds amount
        if self._sum_last_five_exceeds(amount):
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
        text = f"Personal account history:{self.history}"
        
        # Send email using SMTP client
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)         