from src.personal_account import PersonalAccount

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678910"

    # tests for pesel
    def test_pesel_too_short(self):
        account = PersonalAccount("Jane", "Doe", "12345")
        assert account.pesel == "Inavlid"
    
    def test_pesel_too_long(self):
        account = PersonalAccount("Jane", "Doe", "123451234512345")
        assert account.pesel == "Inavlid"

    def test_pesel_non_digit(self):
        account = PersonalAccount("Jane", "Doe", None)
        assert account.pesel == "Inavlid"

    # tests for promo_code 
    # valid
    def test_promo_code_valid_format_adds_50(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="PROM_ABC")
        assert account.balance == 50
    def test_promo_code_valid_format_with_numbers(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="PROM_123")
        assert account.balance == 50.0

    def test_promo_code_valid_format_with_mixed_chars(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="PROM_A1B2C3")
        assert account.balance == 50.0

    # none-valid
    def test_promo_code_invalid_not_is_instance_str(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code=bool(True))
        assert account.balance == 0.0
    def test_promo_code_none_no_bonus(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code=None)
        assert account.balance == 0.0

    def test_promo_code_invalid_format_bad_prefix(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="ABC_123")
        assert account.balance == 0.0

    def test_promo_code_invalid_format_no_underscore(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="PROMABC")
        assert account.balance == 0.0

    def test_promo_code_invalid_format_only_prom(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="PROM_")
        assert account.balance == 0.0

    def test_promo_code_ivalid_format_lowercase(self):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code="prom_abc")
        assert account.balance == 0.0

    # tests of validation participation to promotion
    # participates in promotion
    def test_pesel_valid_participates_in_promo_XXI_century(self):
        account = PersonalAccount("Alice", "Smith", "09876543210", promo_code="PROM_XYZ")
        assert account.pesel == "09876543210"
        assert account.balance == 50.0
        assert account.younger_than_60 == True
    def test_pesel_valid_participates_in_promo_XX_century_over_1960(self):
        account = PersonalAccount("Bob", "Brown", "66012345678", promo_code="PROM_12345")
        assert account.pesel == "66012345678"
        assert account.balance == 50.0
        assert account.younger_than_60 == True
    
    # does not participate in promotion
    def test_pesel_valid_does_not_participate_in_promo_XX_century_under_1960(self):
        account = PersonalAccount("Charlie", "Davis", "59012345678", promo_code="PROM_67890")
        assert account.pesel == "59012345678"
        assert account.balance == 0.0
        assert account.younger_than_60 == False
    def test_pesel_valid_does_not_participate_in_promo_1960_birth_year(self):
        account = PersonalAccount("Eve", "Wilson", "60012345678", promo_code="PROM_EDGE")
        assert account.pesel == "60012345678"
        assert account.balance == 0.0
        assert account.younger_than_60 == False
    def test_pesel_invalid_does_not_participate_in_promo_pesel_invalid(self):
        account = PersonalAccount("Diana", "Evans", "12345", promo_code="PROM_ABCDE")
        assert account.pesel == "Inavlid"
        assert account.balance == 0.0
        assert account.younger_than_60 == False
    
