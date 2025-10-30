# backend/app/routers/servicos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

# Importamos nossos modelos, esquemas e a dependência do banco de dados
from ..database import get_session
from ..models import Profissional
from ..schemas import ProfissionalCreate, ProfissionalRead

# Importamos a dependência de autenticação, que já deve existir em seu projeto
from ..auth import get_current_active_user # Ajuste o path se necessário
from ..models import User # Ajuste o path se necessário

router = APIRouter(
    prefix="/profissionais",
    tags=["Profissionais"],
    dependencies=[Depends(get_current_active_user)],
)

@router.post("/", response_model=ProfissionalRead, status_code=status.HTTP_201_CREATED)
def create_profissional(
    profissional: ProfissionalCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user) # Proteção da rota
):
    db_profissional = Profissional.model_validate(profissional) # Converte o schema para model
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional