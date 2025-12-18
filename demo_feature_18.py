import os
from src.company_account import CompanyAccount

def demo_valid_nip():
    """Przykład z poprawnym, aktywnym NIPem"""
    print("\n" + "="*70)
    print("SCENARIUSZ 1: Poprawny, aktywny NIP")
    print("="*70)
    
    try:
        # NIP firmy Microsoft (przykład z dokumentacji MF)
        account = CompanyAccount("Microsoft Sp. z o.o.", "5252548877")
        print(f"Konto utworzone pomyślnie!")
        print(f"Nazwa: {account.name}")
        print(f"NIP: {account.nip}")
        print(f"Saldo: {account.balance}")
    except ValueError as e:
        print(f"Błąd: {e}")

def demo_invalid_nip():
    """Przykład z niepoprawnym/nieaktywnym NIPem"""
    print("\n" + "="*70)
    print("SCENARIUSZ 2: Niepoprawny lub nieaktywny NIP")
    print("="*70)
    
    try:
        # Losowy NIP który prawdopodobnie nie istnieje
        account = CompanyAccount("Fake Company", "1234567890")
        print(f"Konto utworzone pomyślnie!")
        print(f"Nazwa: {account.name}")
        print(f"NIP: {account.nip}")
    except ValueError as e:
        print(f"Błąd podczas tworzenia konta: {e}")
        print(f"To zachowanie jest poprawne - NIP nie istnieje w bazie MF")

def demo_malformed_nip():
    """Przykład z nieprawidłowym formatem NIPu"""
    print("\n" + "="*70)
    print("SCENARIUSZ 3: Nieprawidłowy format NIPu (za krótki)")
    print("="*70)
    
    try:
        # NIP za krótki - nie wysyła requestu do API
        account = CompanyAccount("Short NIP Company", "12345")
        print(f"Konto utworzone (bez walidacji w API)")
        print(f"Nazwa: {account.name}")
        print(f"NIP: {account.nip}")
        print(f"Saldo: {account.balance}")
        print(f"NIP oznaczony jako 'Invalid' - nie wysłano requestu do API MF")
    except ValueError as e:
        print(f"Błąd: {e}")

def demo_env_variable():
    """Demonstracja użycia zmiennej środowiskowej"""
    print("\n" + "="*70)
    print("SCENARIUSZ 4: Konfiguracja URL przez zmienną środowiskową")
    print("="*70)
    
    current_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
    print(f"Aktualny URL API MF: {current_url}")
    print(f"\nAby zmienić na produkcyjne API, ustaw:")
    print(f"   set BANK_APP_MF_URL=https://wl-api.mf.gov.pl  (Windows)")
    print(f"   export BANK_APP_MF_URL=https://wl-api.mf.gov.pl  (Linux/Mac)")

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# DEMO: Feature 18 - Walidacja NIPu w API Ministerstwa Finansów")
    print("#"*70)
    
    demo_env_variable()
    demo_valid_nip()
    demo_invalid_nip()
    demo_malformed_nip()
    
    print("\n" + "="*70)
    print("DEMO ZAKOŃCZONE")
    print("="*70)
    print("\nWszystkie zapytania do API MF są logowane w konsoli.")
    print("Sprawdź powyższe logi aby zobaczyć odpowiedzi z API.\n")
