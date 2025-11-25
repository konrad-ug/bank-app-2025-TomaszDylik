"""Global pytest fixtures for all test modules."""
import pytest
from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


@pytest.fixture
def base_account():
    return Account()


@pytest.fixture
def personal_account():
    return PersonalAccount("Jan", "Kowalski", "12345678901")


@pytest.fixture
def personal_account_john():
    return PersonalAccount("John", "Doe", "12345678910")


@pytest.fixture
def company_account():
    return CompanyAccount("TechCorp", "1234567890")
