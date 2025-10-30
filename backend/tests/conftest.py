from app.models import User # Importe seu modelo User
from app.database import get_session # Ou Session se for direto
from app.security import hash_password # Importe a função que faz o hash
from app.security import create_access_token # Importe a função que gera o token

import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel  # Importar SQLModel diretamente do sqlmodel

from app.database import engine  # Importar apenas engine do app.database
from app.main import app
from app.models import User  # Importar modelos conforme necessário

# Configurar banco de dados em memória para testes
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Criar tabelas antes dos testes e limpar após"""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def client():
    """Client para testes API"""
    with TestClient(app) as test_client:
        yield test_client



@pytest.fixture(scope="function")
def session_test(client):
    """Fixture que fornece uma sessão de banco de dados para a função de teste."""
    # Como você não tem uma fixture de sessão explícita, podemos usar o 'get_session'
    # para garantir que temos acesso ao banco de testes do TestClient.
    with get_session() as session:
        yield session


@pytest.fixture(scope="function")
def test_user(session_test):
    """Cria e insere um usuário de teste válido no banco de dados temporário."""
    
    # 💡 Lembre-se: Use a senha criptografada que seu sistema espera
    hashed_pass = hash_password("senha-secreta") 

    user = User(
        email="teste@salao.com", 
        hashed_password=hashed_pass, 
        is_active=True, 
        is_superuser=True, 
        nome="Usuário Teste"
    )
    
    session_test.add(user)
    session_test.commit()
    session_test.refresh(user)
    
    return user



@pytest.fixture(scope="function")
def auth_headers(test_user):
    """Retorna os headers de autenticação JWT para um usuário de teste."""
    
    # Geramos um token de acesso usando a função de segurança do seu projeto
    access_token = create_access_token(
        data={"sub": test_user.email},
        # Você pode precisar passar o tempo de expiração, dependendo da sua função
    )
    
    # O formato padrão para JWT em requisições é 'Bearer <token>'
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    return headers