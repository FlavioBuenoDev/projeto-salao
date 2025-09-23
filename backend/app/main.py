from contextlib import asynccontextmanager
from datetime import date, datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, and_, select

from app.database import engine, get_session
from app.models import Agendamento, Cliente
from app.schemas import AgendamentoCreate, AgendamentoRead, ClienteCreate, ClienteRead
from fastapi.middleware.cors import CORSMiddleware

from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth import (
    create_access_token, get_current_user, get_current_active_user,
    require_admin, require_staff, ACCESS_TOKEN_EXPIRE_MINUTES
)

from app.models import User

from app.schemas import (
    UserCreate, UserRead, UserUpdate, Token, LoginRequest, ChangePasswordRequest, LoginResponse, TokenWithUser
)


# Lifespan handler para eventos de startup e shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event - criar tabelas
    print("Iniciando aplicação...")
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown event - limpar recursos se necessário
    print("Encerrando aplicação...")


app = FastAPI(
    title="Sistema de Agendamento - Salão de Beleza",
    description="API para gerenciamento de agendamentos de salão de beleza",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Bem-vindo ao sistema de agendamento!"}


@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Sistema funcionando corretamente"}


# Rotas para Clientes
@app.post(
    "/clientes/",
    response_model=ClienteRead,
    summary="Criar um novo cliente",
    description="Endpoint para cadastrar um novo cliente no sistema",
    response_description="Dados do cliente criado",
)
def criar_cliente(cliente: ClienteCreate, session: Session = Depends(get_session)):
    # Corrigido: Criar instância do modelo Cliente a partir do schema
    db_cliente = Cliente(
        nome=cliente.nome, telefone=cliente.telefone, email=cliente.email
    )
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


@app.get(
    "/clientes/",
    response_model=list[ClienteRead],
    summary="Listar todos os clientes",
    description="Retorna uma lista com todos os clientes cadastrados",
)
def listar_clientes(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente)).all()
    return clientes


@app.get("/clientes/{cliente_id}", response_model=ClienteRead)
def ler_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@app.put("/clientes/{cliente_id}", response_model=ClienteRead)
def atualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteCreate,
    session: Session = Depends(get_session),
):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente.nome = cliente_update.nome
    cliente.telefone = cliente_update.telefone
    cliente.email = cliente_update.email

    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(cliente)
    session.commit()
    return {"message": "Cliente deletado com sucesso"}


# Rotas para Agendamentos (única definição do endpoint criar_agendamento)
@app.post("/agendamentos/", response_model=AgendamentoRead)
def criar_agendamento(
    agendamento: AgendamentoCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    # Verificar se o cliente existe
    cliente = session.get(Cliente, agendamento.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Corrigir a comparação de datas
    agora_utc = datetime.now(timezone.utc)
    data_agendamento = agendamento.data_hora

    # Se a data do agendamento não tem fuso horário, assumir que é UTC
    if data_agendamento.tzinfo is None:
        data_agendamento = data_agendamento.replace(tzinfo=timezone.utc)

    if data_agendamento < agora_utc:
        raise HTTPException(status_code=400, detail="Não é possível agendar no passado")

    # Verificar conflito de horário
    agendamento_existente = session.exec(
        select(Agendamento).where(Agendamento.data_hora == agendamento.data_hora)
    ).first()

    if agendamento_existente:
        raise HTTPException(
            status_code=400, detail="Já existe um agendamento para este horário"
        )

    # Corrigido: Criar instância do modelo Agendamento a partir do schema
    db_agendamento = Agendamento(
        cliente_id=agendamento.cliente_id,
        data_hora=agendamento.data_hora,
        servico=agendamento.servico,
        observacoes=agendamento.observacoes,
    )

    session.add(db_agendamento)
    session.commit()
    session.refresh(db_agendamento)
    return db_agendamento


@app.get("/agendamentos/", response_model=list[AgendamentoRead])
def listar_agendamentos(session: Session = Depends(get_session)):
    agendamentos = session.exec(select(Agendamento)).all()
    return agendamentos


@app.get("/agendamentos/{agendamento_id}", response_model=AgendamentoRead)
def ler_agendamento(agendamento_id: int, session: Session = Depends(get_session)):
    agendamento = session.get(Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento


@app.put("/agendamentos/{agendamento_id}", response_model=AgendamentoRead)
def atualizar_agendamento(
    agendamento_id: int,
    agendamento_data: AgendamentoCreate,
    session: Session = Depends(get_session),
):
    agendamento = session.get(Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    # Verificar se o cliente existe
    cliente = session.get(Cliente, agendamento_data.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    agendamento.cliente_id = agendamento_data.cliente_id
    agendamento.data_hora = agendamento_data.data_hora
    agendamento.servico = agendamento_data.servico
    agendamento.observacoes = agendamento_data.observacoes

    session.add(agendamento)
    session.commit()
    session.refresh(agendamento)
    return agendamento


@app.delete("/agendamentos/{agendamento_id}")
def deletar_agendamento(agendamento_id: int, session: Session = Depends(get_session)):
    agendamento = session.get(Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    session.delete(agendamento)
    session.commit()
    return {"message": "Agendamento deletado com sucesso"}


# Consultas com filtros
@app.get("/agendamentos/cliente/{cliente_id}", response_model=list[AgendamentoRead])
def listar_agendamentos_cliente(
    cliente_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    # Verificar se o cliente existe
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    agendamentos = session.exec(
        select(Agendamento).where(Agendamento.cliente_id == cliente_id)
    ).all()
    return agendamentos


@app.get("/agendamentos/data/{data_consulta}", response_model=list[AgendamentoRead])
def listar_agendamentos_data(
    data_consulta: date, session: Session = Depends(get_session)
):
    # Calcular início e fim do dia
    inicio_dia = datetime.combine(data_consulta, datetime.min.time())
    fim_dia = datetime.combine(data_consulta, datetime.max.time())

    agendamentos = session.exec(
        select(Agendamento).where(
            and_(Agendamento.data_hora >= inicio_dia, Agendamento.data_hora <= fim_dia)
        )
    ).all()
    return agendamentos
# =============================================================================
# ROTAS DE AUTENTICAÇÃO
# =============================================================================

@app.post("/auth/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Registrar um novo usuário
    """
    try:
        # Verificar se o username já existe
        existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso"
            )
        
        # Verificar se o email já existe
        existing_email = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
        
        # Criar o usuário
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role
        )
        
        # Definir a senha (fazer hash)
        db_user.set_password(user_data.password)
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        return db_user
        
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )
        
@app.post("/auth/login", response_model=Token)
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    print(f"Tentativa de login para: {login_data.username}")
    """
    Fazer login e obter token de acesso
    """
    # Buscar usuário pelo username
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    print(f"Usuário encontrado: {user is not None}")
    
    if user:
        print(f"Senha correta: {user.verify_password(login_data.password)}")
        print(f"Usuário ativo: {user.is_active}")
    
    # Verificar se o usuário existe e a senha está correta
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos"
        )
    
    # Verificar se o usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Criar token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
        # Remova a linha abaixo para corresponder ao schema Token
        # "user": user
    }
        
        
@app.post("/auth/login-with-user", response_model=LoginResponse)
def login_with_user(login_data: LoginRequest, session: Session = Depends(get_session)):
    """
    Fazer login e obter token de acesso com informações do usuário
    """
    user = session.exec(select(User).where(User.username == login_data.username)).first()
    
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/auth/me", response_model=UserRead)
async def get_my_info(current_user: User = Depends(get_current_active_user)):
    """
    Obter informações do usuário atual
    """
    return current_user

@app.put("/auth/me", response_model=UserRead)
async def update_my_info(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Atualizar informações do usuário atual
    """
    update_data = user_update.dict(exclude_unset=True)
    
    # Atualizar campos permitidos
    for field, value in update_data.items():
        if field == "password" and value:
            current_user.set_password(value)
        elif hasattr(current_user, field):
            setattr(current_user, field, value)
    
    current_user.update_timestamp()
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return current_user

# =============================================================================
# ROTAS ADMINISTRATIVAS (apenas para administradores)
# =============================================================================

def require_admin(current_user: User = Depends(get_current_active_user)):
    """Verifica se o usuário é administrador"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    return current_user

@app.get("/admin/users", response_model=list[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Listar todos os usuários (apenas admin)"""
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/admin/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Obter informações de um usuário específico (apenas admin)"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

