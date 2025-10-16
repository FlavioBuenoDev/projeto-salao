
import os
from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, and_, select

from app.database import engine, get_session
from app.models import Agendamento, Cliente, User

from app.schemas import (
    AgendamentoCreate, AgendamentoRead, 
    ClienteCreate, ClienteRead, 
    UserCreate, UserRead,  # ← Usar essas
    Token, LoginRequest, LoginResponse  # ← Se necessário
)

# Importar do security.py local
from app.security import (
    verify_password, 
    create_access_token, 
    get_current_user,
    get_password_hash,
    require_admin
)

# Lifespan handler para eventos de startup e shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event - criar tabelas apenas se variável de ambiente estiver definida
    print("Iniciando aplicação...")
    if os.getenv("CREATE_TABLES", "0") == "1":
        SQLModel.metadata.create_all(engine)
        print("Tabelas criadas!")
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

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Verifica se usuário está ativo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user

# =============================================================================
# ROTAS DE AUTENTICAÇÃO
# =============================================================================

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Autentica usuário e retorna token JWT
    """
    # 1. Buscar usuário no banco (usando SQLModel)
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()
    
    # 2. Verificar se usuário existe e senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Criar token JWT
    access_token = create_access_token(data={"sub": user.username})
    
    # 4. Retornar token
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.post("/register")
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Registra novo usuário
    """
    # Verificar se usuário já existe
    statement = select(User).where(
        (User.username == user_data.username) | (User.email == user_data.email)
    )
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username ou email já cadastrado"
        )
    
    # Criar novo usuário
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role or "user",
        is_active=True
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "Usuário criado com sucesso", "user_id": new_user.id}

@app.get("/auth/me")
async def get_my_info(current_user: User = Depends(get_current_active_user)):
    """Obter informações do usuário atual"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }

# =============================================================================
# ROTAS PÚBLICAS
# =============================================================================

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao sistema de agendamento!"}

@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Sistema funcionando corretamente"}

# =============================================================================
# ROTAS PARA CLIENTES (Protegidas)
# =============================================================================

@app.post("/clientes/", 
          response_model=ClienteRead, 
          summary="Criar um novo cliente",
          description="Endpoint para cadastrar um novo cliente no sistema",
          response_description="Dados do cliente criado")
def criar_cliente(
    cliente: ClienteCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    db_cliente = Cliente(
        nome=cliente.nome, 
        telefone=cliente.telefone, 
        email=cliente.email
    )
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/", 
         response_model=list[ClienteRead],
         summary="Listar todos os clientes",
         description="Retorna uma lista com todos os clientes cadastrados")
def listar_clientes(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    clientes = session.exec(select(Cliente)).all()
    return clientes

@app.get("/clientes/{cliente_id}", response_model=ClienteRead)
def ler_cliente(
    cliente_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.put("/clientes/{cliente_id}", response_model=ClienteRead)
def atualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
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
def deletar_cliente(
    cliente_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin)  
):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(cliente)
    session.commit()
    return {"message": "Cliente deletado com sucesso"}

# =============================================================================
# ROTAS PARA AGENDAMENTOS (Protegidas)
# =============================================================================

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
def listar_agendamentos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    agendamentos = session.exec(select(Agendamento)).all()
    return agendamentos

@app.get("/agendamentos/{agendamento_id}", response_model=AgendamentoRead)
def ler_agendamento(
    agendamento_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    agendamento = session.get(Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento

@app.put("/agendamentos/{agendamento_id}", response_model=AgendamentoRead)
def atualizar_agendamento(
    agendamento_id: int,
    agendamento_data: AgendamentoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
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
def deletar_agendamento(
    agendamento_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    agendamento = session.get(Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    session.delete(agendamento)
    session.commit()
    return {"message": "Agendamento deletado com sucesso"}

# =============================================================================
# CONSULTAS COM FILTROS (Protegidas)
# =============================================================================

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
    data_consulta: date, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
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
# ROTAS ADMINISTRATIVAS (Apenas para admin)
# =============================================================================

@app.get("/admin/users")
async def list_users(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Listar todos os usuários (apenas admin)"""
    users = session.exec(select(User)).all()
    return users

@app.get("/admin/health")
async def admin_health_check(current_user: User = Depends(require_admin)):
    """Verificação de saúde para admin"""
    return {"status": "OK", "message": "Admin: Sistema funcionando corretamente"}

@app.get("/admin/stats")
async def admin_stats(
    current_user: User = Depends(require_admin), 
    session: Session = Depends(get_session)
):
    """Estatísticas do sistema (apenas admin)"""
    total_users = session.exec(select(User)).count()
    total_clientes = session.exec(select(Cliente)).count()
    total_agendamentos = session.exec(select(Agendamento)).count()
    
    return {
        "total_users": total_users,
        "total_clientes": total_clientes,
        "total_agendamentos": total_agendamentos
    }

@app.get("/admin/clients")
async def admin_list_clients(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Listar todos os clientes (apenas admin)"""
    clients = session.exec(select(Cliente)).all()
    return clients

@app.get("/admin/appointments")
async def admin_list_appointments(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Listar todos os agendamentos (apenas admin)"""
    appointments = session.exec(select(Agendamento)).all()
    return appointments

@app.delete("/admin/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Deletar um usuário pelo ID (apenas admin)"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado com sucesso"}

@app.delete("/admin/clients/{client_id}")
async def admin_delete_client(
    client_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Deletar um cliente pelo ID (apenas admin)"""
    client = session.get(Cliente, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    session.delete(client)
    session.commit()
    return {"message": "Cliente deletado com sucesso"}

@app.delete("/admin/appointments/{appointment_id}")
async def admin_delete_appointment(
    appointment_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Deletar um agendamento pelo ID (apenas admin)"""
    appointment = session.get(Agendamento, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    session.delete(appointment)
    session.commit()
    return {"message": "Agendamento deletado com sucesso"}


# =============================================================================
# ROTAS RELATÓRIOS (Apenas para admin)
# =============================================================================

# Importações adicionais no topo do main.py
from app.reports import ReportService
from fastapi.responses import StreamingResponse, JSONResponse
import pandas as pd
import io
import csv

# Endpoints de relatórios
@app.get("/admin/reports/stats")
def get_estatisticas_gerais(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Estatísticas gerais do sistema"""
    report_service = ReportService(session)
    return report_service.get_general_stats()

@app.get("/admin/reports/agendamentos-servico")
def get_agendamentos_por_servico(
    dias: int = 30,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Agendamentos agrupados por serviço"""
    report_service = ReportService(session)
    return report_service.get_agendamentos_por_servico(dias)

@app.get("/admin/reports/agendamentos-diarios")
def get_agendamentos_diarios(
    dias: int = 7,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Agendamentos por dia"""
    report_service = ReportService(session)
    return report_service.get_agendamentos_por_dia(dias)

@app.get("/admin/reports/clientes-novos")
def get_clientes_novos(
    dias: int = 30,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Clientes novos por período"""
    report_service = ReportService(session)
    return report_service.get_clientes_novos_por_periodo(dias)

@app.get("/admin/reports/top-clientes")
def get_top_clientes(
    limite: int = 10,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Top clientes"""
    report_service = ReportService(session)
    return report_service.get_top_clientes(limite)

# Endpoint para exportar relatórios em CSV
@app.get("/admin/reports/export/csv")
def exportar_relatorio_csv(
    tipo: str,  # clientes, agendamentos, servicos
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Exportar relatório em CSV"""
    
    # Converter datas
    if data_inicio:
        data_inicio = datetime.fromisoformat(data_inicio.replace('Z', '+00:00'))
    if data_fim:
        data_fim = datetime.fromisoformat(data_fim.replace('Z', '+00:00'))
    
    if tipo == "clientes":
        # Exportar clientes
        clientes = session.exec(select(Cliente)).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Nome', 'Telefone', 'Email', 'Data Cadastro'])
        
        for cliente in clientes:
            writer.writerow([
                cliente.id,
                cliente.nome,
                cliente.telefone,
                cliente.email,
                cliente.created_at.strftime("%d/%m/%Y %H:%M") if cliente.created_at else ""
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=clientes.csv"}
        )
    
    elif tipo == "agendamentos":
        # Exportar agendamentos
        query = select(Agendamento, Cliente).join(Cliente)
        if data_inicio:
            query = query.where(Agendamento.data_hora >= data_inicio)
        if data_fim:
            query = query.where(Agendamento.data_hora <= data_fim)
        
        resultados = session.exec(query).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Cliente', 'Data/Hora', 'Serviço', 'Observações'])
        
        for agendamento, cliente in resultados:
            writer.writerow([
                agendamento.id,
                cliente.nome,
                agendamento.data_hora.strftime("%d/%m/%Y %H:%M"),
                agendamento.servico,
                agendamento.observacoes or ""
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=agendamentos_{datetime.now().strftime('%Y%m%d')}.csv"}
        )
    
    elif tipo == "servicos":
        # Exportar resumo por serviços
        report_service = ReportService(session)
        servicos = report_service.get_agendamentos_por_servico(365)  # Último ano
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Serviço', 'Quantidade', 'Percentual'])
        
        for servico in servicos:
            writer.writerow([
                servico['servico'],
                servico['quantidade'],
                f"{servico['percentual']}%"
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=servicos.csv"}
        )

# Endpoint para dados do dashboard
@app.get("/admin/reports/dashboard")
def get_dashboard_data(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Dados completos para o dashboard"""
    report_service = ReportService(session)
    
    return {
        "estatisticas_gerais": report_service.get_general_stats(),
        "agendamentos_por_servico": report_service.get_agendamentos_por_servico(30),
        "agendamentos_diarios": report_service.get_agendamentos_por_dia(7),
        "clientes_novos": report_service.get_clientes_novos_por_periodo(30),
        "top_clientes": report_service.get_top_clientes(5)
    }