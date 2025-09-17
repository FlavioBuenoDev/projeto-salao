import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel  # Importar SQLModel diretamente do sqlmodel

from app.database import engine  # Importar apenas engine do app.database
from app.main import app

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
