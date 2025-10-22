from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    hashed_password: str
    role: str = Field(default="user") 
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    telefone: str
    email: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Agendamento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    data_hora: datetime
    servico: str
    observacoes: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Servico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    duracao_minutos: int
    preco: float
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ProfissionalServico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profissional_id: int = Field(foreign_key="profissional.id", primary_key=True)
    servico_id: int = Field(foreign_key="servico.id", primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Profissional(SQLModel, table=True):
    id: int | None
    nome: str | None
    email: str | None
    ativo : bool = Field(default=True)
    servicos: list["Servico"] = Relationship(back_populates="profissionais", link_model=ProfissionalServico)
