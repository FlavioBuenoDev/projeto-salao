from fastapi.testclient import TestClient

from app.main import app
from app.models import Cliente

client = TestClient(app)


def test_criar_cliente(client):
    cliente_data = {
        "nome": "Maria Silva",
        "telefone": "11999999999",
        "email": "maria@email.com",
    }
    response = client.post("/clientes/", json=cliente_data)

    # Verificar se a requisição foi bem-sucedida
    assert response.status_code == 200, f"Erro inesperado: {response.text}"

    data = response.json()
    assert data["nome"] == "Maria Silva"
    assert data["email"] == "maria@email.com"
    assert "id" in data
