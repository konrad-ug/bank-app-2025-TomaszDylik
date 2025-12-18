import pytest
from app.api import app, registry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Czyszczenie rejestru przed każdym testem
        registry.accounts.clear()
        yield client


def test_create_account_integration(client):
    payload = {
        "name": "Jan",
        "surname": "Kowalski",
        "pesel": "12345678901"
    }
    
    response = client.post('/api/accounts', json=payload)
    
    assert response.status_code == 201
    assert response.json["message"] == "Account created"


def test_get_all_accounts(client):
    # Tworzymy kilka kont
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": "12345678901"})
    client.post('/api/accounts', json={"name": "Anna", "surname": "Nowak", "pesel": "98765432109"})
    
    response = client.get('/api/accounts')
    
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Jan"
    assert response.json[1]["name"] == "Anna"


def test_get_all_accounts_empty(client):
    response = client.get('/api/accounts')
    
    assert response.status_code == 200
    assert response.json == []


def test_get_account_count(client):
    # Tworzymy kilka kont
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": "12345678901"})
    client.post('/api/accounts', json={"name": "Anna", "surname": "Nowak", "pesel": "98765432109"})
    
    response = client.get('/api/accounts/count')
    
    assert response.status_code == 200
    assert response.json["count"] == 2


def test_get_account_by_pesel(client):
    # Tworzymy konto
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    # Pobieramy konto po peselu
    response = client.get(f'/api/accounts/{pesel}')
    
    assert response.status_code == 200
    assert response.json["name"] == "Jan"
    assert response.json["surname"] == "Kowalski"
    assert response.json["pesel"] == pesel
    assert response.json["balance"] == 0


def test_get_account_by_pesel_not_found(client):
    # Próbujemy pobrać konto, które nie istnieje
    response = client.get('/api/accounts/99999999999')
    
    assert response.status_code == 404
    assert response.json["message"] == "Account not found"


def test_update_account_both(client):
    # Tworzymy konto
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    # Updatujemy imię i nazwisko
    response = client.patch(f'/api/accounts/{pesel}', json={"name": "Janusz", "surname": "Nowak"})
    
    assert response.status_code == 200
    assert response.json["message"] == "Account updated"
    assert response.json["account"]["name"] == "Janusz"
    assert response.json["account"]["surname"] == "Nowak"


def test_delete_account(client):
    # Tworzymy konto
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    # Usuwamy konto
    response = client.delete(f'/api/accounts/{pesel}')
    
    assert response.status_code == 200
    assert response.json["message"] == "Account deleted"
    
    # Sprawdzamy czy konto zostało usunięte
    get_response = client.get(f'/api/accounts/{pesel}')
    assert get_response.status_code == 404

def test_delete_account_not_found(client):
    # Próbujemy usunąć konto, które nie istnieje
    response = client.delete('/api/accounts/99999999999')
    
    assert response.status_code == 404
    assert response.json["message"] == "Account not found"


def test_create_account_with_duplicate_pesel(client):
    # Tworzymy pierwsze konto
    pesel = "12345678901"
    payload = {"name": "Jan", "surname": "Kowalski", "pesel": pesel}
    response1 = client.post('/api/accounts', json=payload)
    assert response1.status_code == 201
    
    # Próbujemy utworzyć drugie konto z tym samym peselem
    payload2 = {"name": "Anna", "surname": "Nowak", "pesel": pesel}
    response2 = client.post('/api/accounts', json=payload2)
    
    assert response2.status_code == 409
    assert response2.json["message"] == "Account with this PESEL already exists"
    
    # Sprawdzamy, że w rejestrze jest tylko jedno konto
    count_response = client.get('/api/accounts/count')
    assert count_response.json["count"] == 1


def test_create_account_with_different_pesels(client):
    # Tworzymy pierwsze konto
    payload1 = {"name": "Jan", "surname": "Kowalski", "pesel": "12345678901"}
    response1 = client.post('/api/accounts', json=payload1)
    assert response1.status_code == 201
    
    # Tworzymy drugie konto z innym peselem
    payload2 = {"name": "Anna", "surname": "Nowak", "pesel": "98765432109"}
    response2 = client.post('/api/accounts', json=payload2)
    
    assert response2.status_code == 201
    assert response2.json["message"] == "Account created"
    
    # Sprawdzamy, że w rejestrze są dwa konta
    count_response = client.get('/api/accounts/count')
    assert count_response.json["count"] == 2


# FEATURE 17: Transfer tests
@pytest.fixture
def account_with_balance(client):
    """Fixture creating an account with initial balance"""
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    # Add initial balance through incoming transfer
    client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 1000, "type": "incoming"})
    return pesel


def test_transfer_account_not_found(client):
    """Test 1: Sprawdzamy czy zwracamy 404 dla nieistniejącego konta"""
    pesel = "99999999999"
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 100, "type": "incoming"})
    
    assert response.status_code == 404
    assert response.json["message"] == "Account not found"


def test_transfer_invalid_type(client):
    """Test 2: Sprawdzamy czy zwracamy 400 dla nieprawidłowego typu przelewu"""
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 100, "type": "unknown"})
    
    assert response.status_code == 400
    assert response.json["message"] == "Invalid transfer type"


def test_incoming_transfer_success(client):
    """Test 3: Sprawdzamy czy przelew przychodzący działa poprawnie"""
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 500, "type": "incoming"})
    
    assert response.status_code == 200
    assert response.json["message"] == "Zlecenie przyjęto do realizacji"
    
    # Sprawdzamy czy saldo się zmieniło
    account_response = client.get(f'/api/accounts/{pesel}')
    assert account_response.json["balance"] == 500


def test_outgoing_transfer_success(client, account_with_balance):
    """Test 4: Sprawdzamy czy przelew wychodzący działa poprawnie przy wystarczającym saldzie"""
    pesel = account_with_balance
    
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 300, "type": "outgoing"})
    
    assert response.status_code == 200
    assert response.json["message"] == "Zlecenie przyjęto do realizacji"
    
    # Sprawdzamy czy saldo się zmniejszyło
    account_response = client.get(f'/api/accounts/{pesel}')
    assert account_response.json["balance"] == 700  # 1000 - 300


def test_outgoing_transfer_insufficient_funds(client):
    """Test 5: Sprawdzamy czy zwracamy 422 gdy brak środków na koncie"""
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 500, "type": "outgoing"})
    
    assert response.status_code == 422
    assert response.json["message"] == "Insufficient funds"
    
    # Sprawdzamy czy saldo się nie zmieniło
    account_response = client.get(f'/api/accounts/{pesel}')
    assert account_response.json["balance"] == 0


def test_express_transfer_success(client, account_with_balance):
    """Test 6: Sprawdzamy czy przelew ekspresowy działa poprawnie"""
    pesel = account_with_balance
    
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 200, "type": "express"})
    
    assert response.status_code == 200
    assert response.json["message"] == "Zlecenie przyjęto do realizacji"
    
    # Sprawdzamy czy saldo się zmniejszyło o kwotę + opłatę (1.0)
    account_response = client.get(f'/api/accounts/{pesel}')
    assert account_response.json["balance"] == 799  # 1000 - 200 - 1


def test_express_transfer_insufficient_funds(client):
    """Test 7: Sprawdzamy czy zwracamy 422 dla przelewu ekspresowego bez środków"""
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 100, "type": "express"})
    
    assert response.status_code == 422
    assert response.json["message"] == "Insufficient funds"


def test_multiple_transfers_on_same_account(client):
    """Test 8: Sprawdzamy czy można wykonać wiele przelewów na tym samym koncie"""
    pesel = "12345678901"
    client.post('/api/accounts', json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
    
    # Kilka przelewów przychodzących
    client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 100, "type": "incoming"})
    client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 200, "type": "incoming"})
    client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 300, "type": "incoming"})
    
    # Przelew wychodzący
    response = client.post(f'/api/accounts/{pesel}/transfer', json={"amount": 150, "type": "outgoing"})
    
    assert response.status_code == 200
    
    # Sprawdzamy końcowe saldo
    account_response = client.get(f'/api/accounts/{pesel}')
    assert account_response.json["balance"] == 450  # 100 + 200 + 300 - 150

