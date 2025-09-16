from contextlib import asynccontextmanager
from datetime import date, datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, and_, select

from app.database import engine, get_session
from app.models import Agendamento, Cliente
from app.schemas import AgendamentoCreate, AgendamentoRead, ClienteCreate, ClienteRead


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
    allow_origins=["*"],
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
    agendamento: AgendamentoCreate, session: Session = Depends(get_session)
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
    cliente_id: int, session: Session = Depends(get_session)
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
