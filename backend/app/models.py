from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime

class Cliente(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    telefone: str
    email: str

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


    