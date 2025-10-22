class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None, younger_than_60=True):
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
        
        if year_prefix > 60:
            return True
        
        return False
