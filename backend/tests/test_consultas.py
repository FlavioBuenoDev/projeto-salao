
from datetime import date, datetime, timedelta
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

def test_agendamentos_por_cliente():
    headers = get_auth_headers()
    # Criar cliente
    cliente_data = {
        "nome": "Ana Costa",
        "telefone": "11977777777",
        "email": "ana@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data, headers=headers)
    cliente_id = cliente_response.json()["id"]

    # Criar agendamento
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": amanha.isoformat(),
        "servico": "Manicure",
    }
    client.post("/agendamentos/", json=agendamento_data, headers=headers)

    # Consultar agendamentos do cliente
    response = client.get(f"/agendamentos/cliente/{cliente_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["cliente_id"] == cliente_id

def test_agendamentos_por_data():
    headers = get_auth_headers()
    hoje = date.today()
    response = client.get(f"/agendamentos/data/{hoje}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
