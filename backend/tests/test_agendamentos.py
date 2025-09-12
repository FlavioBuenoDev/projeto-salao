from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_criar_agendamento():
    # Primeiro criar um cliente
    cliente_data = {
        "nome": "Carlos Santos",
        "telefone": "11988888888",
        "email": "carlos@email.com"
    }
    cliente_response = client.post("/clientes/", json=cliente_data)
    cliente_id = cliente_response.json()["id"]
    
    # Agora criar agendamento
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": cliente_id,
        "data_hora": amanha.isoformat(),
        "servico": "Corte de Cabelo",
        "observacoes": "Prefere a cadeira perto da janela"
    }
    
    response = client.post("/agendamentos/", json=agendamento_data)
    assert response.status_code == 200
    data = response.json()
    assert data["servico"] == "Corte de Cabelo"
    assert "id" in data

def test_agendamento_cliente_inexistente():
    amanha = datetime.now() + timedelta(days=1)
    agendamento_data = {
        "cliente_id": 999,  # ID que não existe
        "data_hora": amanha.isoformat(),
        "servico": "Corte de Cabelo"
    }
    
    response = client.post("/agendamentos/", json=agendamento_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"