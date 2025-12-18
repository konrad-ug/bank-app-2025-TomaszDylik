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

