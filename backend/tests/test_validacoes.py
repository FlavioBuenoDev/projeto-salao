
from datetime import datetime, timedelta
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

def test_agendamento_no_passado():
    headers = get_auth_headers()
    # Criar cliente
    cliente_data = {
        "nome": "Pedro Alves",
        "telefone": "11966666666",
        "email": "pedro@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data, headers=headers)
    cliente_id = cliente_response.json()["id"]

    # Tentar agendar no passado
    ontem = datetime.now() - timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": ontem.isoformat(),
        "servico": "Corte de Cabelo",
    }

    response = client.post("/agendamentos/", json=agendamento_data, headers=headers)
    assert response.status_code == 400
    assert "passado" in response.json()["detail"].lower()

def test_conflito_horario():
    headers = get_auth_headers()
    # Criar cliente
    cliente_data = {
        "nome": "Julia Lima",
        "telefone": "11955555555",
        "email": "julia@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data, headers=headers)
    cliente_id = cliente_response.json()["id"]

    # Criar primeiro agendamento
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": amanha.isoformat(),
        "servico": "Manicure",
    }
    client.post("/agendamentos/", json=agendamento_data, headers=headers)

    # Tentar criar segundo agendamento no mesmo horário
    response = client.post("/agendamentos/", json=agendamento_data, headers=headers)
    assert response.status_code == 400
    assert (
        "conflito" in response.json()["detail"].lower()
        or "horário" in response.json()["detail"].lower()
    )
