
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    user_data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "user"
    }
    client.post("/register", json=user_data)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    login_response = client.post("/login", data=login_data)
    token = login_response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

def test_criar_cliente():
    headers = get_auth_headers()
    cliente_data = {
        "nome": "Maria Silva",
        "telefone": "11999999999",
        "email": "maria@email.com",
    }
    response = client.post("/clientes/", json=cliente_data, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    assert response.status_code == 200, f"Erro inesperado: {response.text}"

    data = response.json()
    assert data["nome"] == "Maria Silva"
    assert data["email"] == "maria@email.com"
    assert "id" in data
