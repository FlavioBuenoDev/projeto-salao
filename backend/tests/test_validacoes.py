from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)


def test_agendamento_no_passado():
    # Criar cliente
    cliente_data = {
        "nome": "Pedro Alves",
        "telefone": "11966666666",
        "email": "pedro@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data)
    cliente_id = cliente_response.json()["id"]

    # Tentar agendar no passado
    ontem = datetime.now() - timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": ontem.isoformat(),
        "servico": "Corte de Cabelo",
    }

    response = client.post("/agendamentos/", json=agendamento_data)
    assert response.status_code == 400
    assert "passado" in response.json()["detail"].lower()


def test_conflito_horario():
    # Criar cliente
    cliente_data = {
        "nome": "Julia Lima",
        "telefone": "11955555555",
        "email": "julia@email.com",
    }
    cliente_response = client.post("/clientes/", json=cliente_data)
    cliente_id = cliente_response.json()["id"]

    # Criar primeiro agendamento
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": amanha.isoformat(),
        "servico": "Manicure",
    }
    client.post("/agendamentos/", json=agendamento_data)

    # Tentar criar segundo agendamento no mesmo horário
    response = client.post("/agendamentos/", json=agendamento_data)
    assert response.status_code == 400
    assert (
        "conflito" in response.json()["detail"].lower()
        or "horário" in response.json()["detail"].lower()
    )
