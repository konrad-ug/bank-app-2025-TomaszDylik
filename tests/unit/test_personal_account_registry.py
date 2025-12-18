from src.personal_account_registry import AccountRegistry
from src.personal_account import PersonalAccount
import pytest

@pytest.fixture
def empty_registry():
    return AccountRegistry()

@pytest.fixture
def john_account():
    return PersonalAccount("John", "Doe", "12345678910")

@pytest.fixture
def jane_account():
    return PersonalAccount("Jane", "Smith", "09876543210")

@pytest.fixture
def registry_with_two_accounts(empty_registry, john_account, jane_account):
    empty_registry.add_account(john_account)
    empty_registry.add_account(jane_account)
    return empty_registry

class TestAccountRegistry:

    def test_add_personal_account(self, empty_registry, john_account):
        empty_registry.add_account(john_account)
        assert empty_registry.length() == 1
        assert empty_registry.return_all_accounts()[0] == john_account
    
    def test_find_account_by_pesel(self, registry_with_two_accounts, jane_account):
        found_account = registry_with_two_accounts.find_account_by_pesel("09876543210")
        assert found_account == jane_account
        
        not_found_account = registry_with_two_accounts.find_account_by_pesel("11111111111")
        assert not_found_account is None

    def test_return_all_accounts(self, registry_with_two_accounts, john_account, jane_account):
        all_accounts = registry_with_two_accounts.return_all_accounts()
        assert len(all_accounts) == 2
        assert john_account in all_accounts
        assert jane_account in all_accounts

    def test_pesel_exists_when_pesel_is_in_registry(self, registry_with_two_accounts):
        assert registry_with_two_accounts.pesel_exists("12345678910") == True
        assert registry_with_two_accounts.pesel_exists("09876543210") == True

    def test_pesel_exists_when_pesel_not_in_registry(self, empty_registry):
        assert empty_registry.pesel_exists("11111111111") == False

    def test_pesel_exists_after_adding_account(self, empty_registry, john_account):
        assert empty_registry.pesel_exists("12345678910") == False
        empty_registry.add_account(john_account)
        assert empty_registry.pesel_exists("12345678910") == True

