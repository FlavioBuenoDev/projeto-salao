from fastapi.testclient import TestClient
from app.schemas import ServicoCreate 

PAYLOAD_SERVICO_VALIDO = {
    "nome": "Corte Feminino",
    "descricao": "Corte com acabamento moderno",
    "duracao_minutos": 60,
    "preco": 120.00
}

# Note como passamos 'client' e 'auth_headers' como argumentos.
# O Pytest encontra as fixtures no conftest.py e as injeta aqui.
def test_create_servico_success(client: TestClient, auth_headers: dict):
    """Testa a criação bem-sucedida de um novo serviço com autenticação."""

    url = "/servicos/"
    
    # ACT (Agir): Simular a requisição HTTP POST
    response = client.post(
        url, 
        json=PAYLOAD_SERVICO_VALIDO, 
        headers=auth_headers # 👈 USANDO O CABEÇALHO AQUI!
    )

    # ASSERT (Verificar)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == PAYLOAD_SERVICO_VALIDO["nome"]
    assert "id" in data

# Teste de falha (já que não usamos 'auth_headers', ele não envia o token)
def test_create_servico_unauthorized(client: TestClient):
    """Testa se a criação de serviço falha sem token de autenticação."""

    url = "/servicos/"
    response = client.post(url, json=PAYLOAD_SERVICO_VALIDO)

    assert response.status_code == 401 # Unauthorized (Não Autorizado)