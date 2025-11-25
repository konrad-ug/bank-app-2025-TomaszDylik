import pytest
from src.personal_account import PersonalAccount


class TestPersonalAccountCreation:
    
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678910"


class TestPeselValidation:
    
    @pytest.mark.parametrize("pesel,expected_pesel", [
        ("12345", "Inavlid"),  # too short
        ("123451234512345", "Inavlid"),  # too long
        (None, "Inavlid"),  # non-digit (None)
    ])
    def test_invalid_pesel(self, pesel, expected_pesel):
        account = PersonalAccount("Jane", "Doe", pesel)
        assert account.pesel == expected_pesel


class TestPromoCodeValidation:
    
    @pytest.mark.parametrize("promo_code,expected_balance", [
        # Valid promo codes - should add 50.0
        ("PROM_ABC", 50.0),
        ("PROM_123", 50.0),
        ("PROM_A1B2C3", 50.0),
        # Invalid promo codes - should not add bonus
        (bool(True), 0.0),  # not a string
        (None, 0.0),  # None
        ("ABC_123", 0.0),  # bad prefix
        ("PROMABC", 0.0),  # no underscore
        ("PROM_", 0.0),  # only prefix
        ("prom_abc", 0.0),  # lowercase
    ])
    def test_promo_code_validation(self, promo_code, expected_balance):
        account = PersonalAccount("John", "Doe", "12345678910", promo_code=promo_code)
        assert account.balance == expected_balance


class TestPromotionEligibility:
    
    @pytest.mark.parametrize("first_name,last_name,pesel,promo_code,expected_pesel,expected_balance,expected_eligible", [
        # Eligible - XXI century (month >= 20)
        ("Alice", "Smith", "09876543210", "PROM_XYZ", "09876543210", 50.0, True),
        # Eligible - XX century born after 1965
        ("Bob", "Brown", "66012345678", "PROM_12345", "66012345678", 50.0, True),
        # Not eligible - XX century born before 1960
        ("Charlie", "Davis", "59012345678", "PROM_67890", "59012345678", 0.0, False),
        # Not eligible - born in 1960
        ("Eve", "Wilson", "60012345678", "PROM_EDGE", "60012345678", 0.0, False),
        # Not eligible - invalid PESEL
        ("Diana", "Evans", "12345", "PROM_ABCDE", "Inavlid", 0.0, False),
    ])
    def test_promotion_eligibility(self, first_name, last_name, pesel, promo_code, 
                                   expected_pesel, expected_balance, expected_eligible):
        account = PersonalAccount(first_name, last_name, pesel, promo_code=promo_code)
        assert account.pesel == expected_pesel
        assert account.balance == expected_balance
        assert account.younger_than_60 == expected_eligible
    
