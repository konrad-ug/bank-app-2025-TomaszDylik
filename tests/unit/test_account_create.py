from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678910"

    # tests for pesel
    def test_pesel_too_short(self):
        account = Account("Jane", "Doe", "12345")
        assert account.pesel == "Inavlid"
    
    def test_pesel_too_long(self):
        account = Account("Jane", "Doe", "123451234512345")
        assert account.pesel == "Inavlid"

    def test_pesel_non_digit(self):
        account = Account("Jane", "Doe", None)
        assert account.pesel == "Inavlid"

    # tests for promo_code 
    # valid
    def test_promo_code_valid_format_adds_50(self):
        account = Account("John", "Doe", "12345678910", promo_code="PROM_ABC")
        assert account.balance == 50.0

    def test_promo_code_valid_format_with_numbers(self):
        account = Account("John", "Doe", "12345678910", promo_code="PROM_123")
        assert account.balance == 50.0

    def test_promo_code_valid_format_with_mixed_chars(self):
        account = Account("John", "Doe", "12345678910", promo_code="PROM_A1B2C3")
        assert account.balance == 50.0

    # none-valid
    def test_promo_code_none_no_bonus(self):
        account = Account("John", "Doe", "12345678910", promo_code=None)
        assert account.balance == 0.0

    def test_promo_code_invalid_format_bad_prefix(self):
        account = Account("John", "Doe", "12345678910", promo_code="ABC_123")
        assert account.balance == 0.0

    def test_promo_code_invalid_format_no_underscore(self):
        account = Account("John", "Doe", "12345678910", promo_code="PROMABC")
        assert account.balance == 0.0

    def test_promo_code_invalid_format_only_prom(self):
        account = Account("John", "Doe", "12345678910", promo_code="PROM_")
        assert account.balance == 0.0

    def test_promo_code_ivalid_format_lowercase(self):
        account = Account("John", "Doe", "12345678910", promo_code="prom_abc")
        assert account.balance == 0.0
