from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Schemas para Cliente
class ClienteBase(BaseModel):
    nome: str
    telefone: str
    email: EmailStr

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int
    
    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True
        
