from datetime import datetime

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel  # type: ignore


class Cliente(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    telefone: str
    email: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, v):
        if "@" not in v:
            raise ValueError("Email inválido")
        return v


class Agendamento(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    data_hora: datetime
    servico: str


class Servico(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    duracao_minutos: int
    preco: float


class ClienteCreate(SQLModel):
    nome: str
    telefone: str
    email: str


class ClienteRead(SQLModel):
    id: int
    nome: str
    telefone: str
    email: str
