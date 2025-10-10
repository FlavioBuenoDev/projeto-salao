from datetime import datetime, timedelta


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    # Cria usuário de teste
    user_data = {
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "user"
    }
    client.post("/register", json=user_data)
    # Realiza login
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    login_response = client.post("/login", data=login_data)
    token = login_response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


def test_criar_agendamento():
    headers = get_auth_headers()
    # Primeiro criar um cliente
    cliente_data = {
        "nome": "Carlos Santos",
        "telefone": "11988888888",
        "email": "carlos@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data, headers=headers)
    cliente_id = cliente_response.json()["id"]

    # Agora criar agendamento
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": amanha.isoformat(),
        "servico": "Corte de Cabelo",
        "observacoes": "Prefere a cadeira perto da janela",
    }

    response = client.post("/agendamentos/", json=agendamento_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["servico"] == "Corte de Cabelo"
    assert "id" in data


def test_agendamento_cliente_inexistente():
    headers = get_auth_headers()
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": 999,  # ID que não existe
        "data_hora": amanha.isoformat(),
        "servico": "Corte de Cabelo",
    }

    response = client.post("/agendamentos/", json=agendamento_data, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"
