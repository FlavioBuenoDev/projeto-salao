from datetime import datetime

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator
import bcrypt


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
    


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str = Field(default="")  # Adicione default vazio
    full_name: str
    role: str = Field(default="user")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Método para definir a senha (fazer hash)
    def set_password(self, password: str):
        """Define a senha do usuário (faz o hash)"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # Método para verificar a senha
    def verify_password(self, password: str) -> bool:
        """Verifica se a senha está correta"""
        if not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except Exception:
            return False

    # Método para atualizar timestamp
    def update_timestamp(self):
        """Atualiza o timestamp de modificação"""
        self.updated_at = datetime.now()