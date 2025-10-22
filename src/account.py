class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Inavlid"
        if self.is_promo_code_valid(promo_code):
            self.promo_code = promo_code
            self.balance += 50.0
        else:
            self.promo_code = None
    
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
