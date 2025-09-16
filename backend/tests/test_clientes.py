from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_criar_cliente():
    cliente_data = {
        "nome": "Maria Silva",
        "telefone": "11999999999",
        "email": "maria@email.com",
    }
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Maria Silva"
    assert data["email"] == "maria@email.com"
    assert "id" in data


def test_listar_clientes():
    response = client.get("/clientes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_email_invalido():
    cliente_data = {
        "nome": "João Silva",
        "telefone": "11999999999",
        "email": "email-invalido",
    }
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 422  # Unprocessable Entity


# teste de atualização de cliente
def test_atualizar_cliente():
    # Primeiro criar um cliente
    cliente_data = {
        "nome": "Ana Souza",
        "telefone": "11977777777",
        "email": "email2@email.com.br",
    }
    response = client.post("/clientes/", json=cliente_data)
    cliente_id = response.json()["id"]

    # Agora atualizar o cliente
    updated_data = {
        "nome": "Ana Souza Atualizada",
        "telefone": "11988888888",
        "email": "email3@email.com.br",
    }
    response = client.put(f"/clientes/{cliente_id}", json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["nome"] == "Ana Souza Atualizada"
    assert data["telefone"] == "11988888888"
    assert data["email"] == "email3@email.com.br"
    assert data["id"] == cliente_id
