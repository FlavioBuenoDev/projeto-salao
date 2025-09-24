from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

# =============================================================================
# SCHEMAS PARA USER (Usando SQLModel para consistência)
# =============================================================================

class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"

class UserRead(SQLModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool

class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

# =============================================================================
# SCHEMAS PARA CLIENTE (Usando SQLModel)
# =============================================================================

class ClienteCreate(SQLModel):
    nome: str
    telefone: str
    email: str

class ClienteRead(SQLModel):
    id: int
    nome: str
    telefone: str
    email: str

# =============================================================================
# SCHEMAS PARA AGENDAMENTO (Usando SQLModel)
# =============================================================================

class AgendamentoCreate(SQLModel):
    cliente_id: int
    data_hora: datetime
    servico: str
    observacoes: Optional[str] = None

class AgendamentoRead(SQLModel):
    id: int
    cliente_id: int
    data_hora: datetime
    servico: str
    observacoes: Optional[str] = None
    cliente: ClienteRead  # ⚠️ Remover por enquanto para evitar recursão

# =============================================================================
# SCHEMAS PARA AUTENTICAÇÃO (Usando SQLModel)
# =============================================================================

class Token(SQLModel):
    access_token: str
    token_type: str

class LoginRequest(SQLModel):
    username: str
    password: str

class ChangePasswordRequest(SQLModel):
    current_password: str
    new_password: str

class LoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: UserRead