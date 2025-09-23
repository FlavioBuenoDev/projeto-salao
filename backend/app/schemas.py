from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


# Schemas para Cliente
class ClienteBase(BaseModel):
    nome: str
    telefone: str
    email: EmailStr


class ClienteCreate(ClienteBase):
    pass


class ClienteRead(ClienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Schemas para Agendamento
class AgendamentoBase(BaseModel):
    cliente_id: int
    data_hora: datetime
    servico: str
    observacoes: Optional[str] = None


class AgendamentoCreate(AgendamentoBase):
    pass


class AgendamentoRead(AgendamentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
    
# Schemas para User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "user"
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Schemas para Autenticação
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class TokenWithUser(Token):
    user: UserRead

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead