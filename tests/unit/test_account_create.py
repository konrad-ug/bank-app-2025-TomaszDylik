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

    # tests of validation participation to promotion
    # participates in promotion
    def test_pesel_valid_participates_in_promo_XXI_century(self):
        account = Account("Alice", "Smith", "09876543210", promo_code="PROM_XYZ")
        assert account.pesel == "09876543210"
        assert account.balance == 50.0
        assert account.younger_than_60 == True
    def test_pesel_valid_participates_in_promo_XX_century_over_1960(self):
        account = Account("Bob", "Brown", "61012345678", promo_code="PROM_12345")
        assert account.pesel == "61012345678"
        assert account.balance == 50.0
        assert account.younger_than_60 == True
    
    # does not participate in promotion
    def test_pesel_valid_does_not_participate_in_promo_XX_century_under_1960(self):
        account = Account("Charlie", "Davis", "59012345678", promo_code="PROM_67890")
        assert account.pesel == "59012345678"
        assert account.balance == 0.0
        assert account.younger_than_60 == False
    def test_pesel_valid_does_not_participate_in_promo_1960_birth_year(self):
        account = Account("Eve", "Wilson", "60012345678", promo_code="PROM_EDGE")
        assert account.pesel == "60012345678"
        assert account.balance == 0.0
        assert account.younger_than_60 == False
    def test_pesel_invalid_does_not_participate_in_promo_pesel_invalid(self):
        account = Account("Diana", "Evans", "12345", promo_code="PROM_ABCDE")
        assert account.pesel == "Inavlid"
        assert account.balance == 0.0
        assert account.younger_than_60 == False
    
