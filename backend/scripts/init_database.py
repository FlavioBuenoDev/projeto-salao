


# ==============================================================================
# ARQUIVO 4: backend/scripts/init_database.py
# ==============================================================================
"""
Script para inicializar banco de dados
Execute: python scripts/init_database.py
"""

import os
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
from sqlmodel import SQLModel
from app.database import engine
from app.models import User, Cliente, Agendamento
from app.security import get_password_hash

def criar_tabelas():
    """Criar todas as tabelas"""
    print("\n📦 Criando tabelas...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tabelas criadas!\n")

def criar_usuario_admin():
    """Criar usuário admin padrão"""
    from sqlmodel import Session, select
    
    print("👤 Criando usuário admin...")
    
    with Session(engine) as session:
        # Verificar se já existe
        statement = select(User).where(User.username == "admin")
        existing = session.exec(statement).first()
        
        if existing:
            print("⚠️  Usuário admin já existe!\n")
            return
        
        # Criar novo admin
        admin = User(
            username="admin",
            email="admin@salao.com",
            full_name="Administrador",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        
        session.add(admin)
        session.commit()
        
        print("✅ Usuário admin criado!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   ⚠️  MUDE A SENHA EM PRODUÇÃO!\n")

def init_database():
    """Inicializar banco de dados completo"""
    
    # Carregar .env
    load_dotenv()
    
    print("\n" + "=" * 60)
    print("🗄️  INICIALIZAÇÃO DO BANCO DE DADOS")
    print("=" * 60)
    
    db_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
    print(f"\n📍 Banco: {db_url}\n")
    
    try:
        criar_tabelas()
        criar_usuario_admin()
        
        print("=" * 60)
        print("✅ Banco de dados inicializado com sucesso!")
        print("=" * 60 + "\n")
        
        print("🚀 Próximo passo:")
        print("   uvicorn app.main:app --reload\n")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)