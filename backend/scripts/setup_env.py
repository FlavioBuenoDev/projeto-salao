# ==============================================================================
# ARQUIVO 1: backend/scripts/setup_env.py
# ==============================================================================
"""
Script para configurar variáveis de ambiente automaticamente
Execute: python scripts/setup_env.py
"""

import secrets
import os
from pathlib import Path

def gerar_secret_key():
    """Gera uma chave secreta forte"""
    return secrets.token_urlsafe(32)

def criar_env_file():
    """Cria arquivo .env baseado no template"""
    
    root_dir = Path(__file__).parent.parent.parent
    env_file = root_dir / ".env"
    env_example = root_dir / ".env.example"
    
    if env_file.exists():
        resposta = input("⚠️  Arquivo .env já existe. Sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada.")
            return
    
    # Gerar nova SECRET_KEY
    secret_key = gerar_secret_key()
    
    print("\n🔧 Configurando ambiente de desenvolvimento...\n")
    
    # Coletar informações
    company_name = input("Nome da empresa (Salão de Beleza): ").strip() or "Salão de Beleza"
    email_from = input("Email remetente (dev@meusalao.com): ").strip() or "dev@meusalao.com"
    
    # Conteúdo do .env
    env_content = f"""# Gerado automaticamente em {Path.cwd()}
# NÃO COMMITAR ESTE ARQUIVO NO GIT!

# DATABASE
DATABASE_URL=sqlite:///database.db

# SECURITY
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API CONFIG
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# FRONTEND
APP_URL=http://localhost:5173
COMPANY_NAME={company_name}

# EMAIL
SENDGRID_API_KEY=sua_sendgrid_key_aqui
EMAIL_FROM={email_from}

# ENVIRONMENT
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG

# MONITORING
SENTRY_DSN=

# BACKUP
BACKUP_ENABLED=False
BACKUP_RETENTION_DAYS=7
"""
    
    # Escrever arquivo
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"\n✅ Arquivo .env criado com sucesso!")
    print(f"📁 Localização: {env_file}")
    print(f"\n🔑 SECRET_KEY gerada: {secret_key[:20]}...")
    print("\n⚠️  IMPORTANTE:")
    print("   1. Adicione .env no .gitignore")
    print("   2. Configure SendGrid API Key se for usar email")
    print("   3. Para produção, gere nova SECRET_KEY!\n")

def criar_frontend_env():
    """Cria .env para o frontend"""
    
    root_dir = Path(__file__).parent.parent.parent
    frontend_dir = root_dir / "frontend"
    env_file = frontend_dir / ".env"
    
    if not frontend_dir.exists():
        print("⚠️  Pasta frontend não encontrada")
        return
    
    if env_file.exists():
        resposta = input("⚠️  Frontend .env já existe. Sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada.")
            return
    
    env_content = """# Frontend Environment Variables
# Todas devem começar com VITE_

VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Sistema de Agendamento
VITE_COMPANY_NAME=Salão de Beleza
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_NOTIFICATIONS=false
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"\n✅ Frontend .env criado!")
    print(f"📁 Localização: {env_file}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Setup de Ambiente - Sistema de Agendamento")
    print("=" * 60)
    
    criar_env_file()
    criar_frontend_env()
    
    print("=" * 60)
    print("✨ Setup concluído!")
    print("=" * 60)
    print("\n📝 Próximos passos:")
    print("   1. cd backend")
    print("   2. pip install -r requirements.txt")
    print("   3. uvicorn app.main:app --reload")
    print("\n   4. cd ../frontend")
    print("   5. npm install")
    print("   6. npm run dev")
    print("=" * 60 + "\n")


