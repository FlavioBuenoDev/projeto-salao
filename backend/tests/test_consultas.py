from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, date, timedelta

client = TestClient(app)


def test_agendamentos_por_cliente():
    # Criar cliente
    cliente_data = {
        "nome": "Ana Costa",
        "telefone": "11977777777",
        "email": "ana@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data)
    cliente_id = cliente_response.json()["id"]

    # Criar agendamento
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": amanha.isoformat(),
        "servico": "Manicure",
    }
    client.post("/agendamentos/", json=agendamento_data)

    # Consultar agendamentos do cliente
    response = client.get(f"/agendamentos/cliente/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["cliente_id"] == cliente_id


def test_agendamentos_por_data():
    hoje = date.today()
    response = client.get(f"/agendamentos/data/{hoje}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
