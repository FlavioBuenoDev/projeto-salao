from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_cliente():
    cliente_data = {
        "nome": "Maria Silva",
        "telefone": "11999999999",
        "email": "maria@email.com"
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
        "email": "email-invalido"
    }
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 422  # Unprocessable Entity