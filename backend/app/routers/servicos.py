# backend/app/routers/servicos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

# Importamos nossos modelos, esquemas e a dependência do banco de dados
from ..database import get_session
from ..models import Servico
from ..schemas import ServicoCreate, ServicoRead

# Importamos a dependência de autenticação, que já deve existir em seu projeto
from ..auth import get_current_active_user # Ajuste o path se necessário
from ..models import User # Ajuste o path se necessário


router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"],
    dependencies=[Depends(get_current_active_user)],
)

@router.post("/", response_model=ServicoRead, status_code=status.HTTP_201_CREATED)
def create_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user) # Proteção da rota
):
    # Lógica para criar o Serviço
    db_servico = Servico.model_validate(servico) # Converte o schema para model
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

