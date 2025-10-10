
# ==============================================================================
# ARQUIVO 2: backend/scripts/check_env.py
# ==============================================================================
"""
Script para validar configuração do ambiente
Execute: python scripts/check_env.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def check_env_vars():
    """Verifica se variáveis essenciais estão configuradas"""
    
    # Carregar .env
    load_dotenv()
    
    print("\n" + "=" * 60)
    print("🔍 VERIFICANDO CONFIGURAÇÃO DO AMBIENTE")
    print("=" * 60 + "\n")
    
    # Variáveis essenciais
    required_vars = {
        'DATABASE_URL': 'URL do banco de dados',
        'SECRET_KEY': 'Chave secreta para JWT',
        'ENVIRONMENT': 'Ambiente (development/production)',
    }
    
    optional_vars = {
        'SENDGRID_API_KEY': 'Chave do SendGrid (email)',
        'SENTRY_DSN': 'DSN do Sentry (monitoramento)',
        'CORS_ORIGINS': 'URLs permitidas (CORS)',
    }
    
    issues = []
    warnings = []
    
    # Verificar variáveis obrigatórias
    print("📋 Variáveis Obrigatórias:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mascarar valores sensíveis
            if 'KEY' in var or 'SECRET' in var:
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            
            print(f"   ✅ {var}: {display_value}")
            
            # Verificações específicas
            if var == 'SECRET_KEY' and len(value) < 32:
                warnings.append(f"⚠️  {var} muito curta (< 32 caracteres)")
            
        else:
            print(f"   ❌ {var}: NÃO CONFIGURADA")
            issues.append(f"{var}: {description}")
    
    # Verificar variáveis opcionais
    print("\n📋 Variáveis Opcionais:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            if 'KEY' in var or 'DSN' in var:
                display_value = value[:10] + "..."
            else:
                display_value = value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ⚠️  {var}: Não configurada ({description})")
    
    # Verificar ambiente
    print("\n🌍 Ambiente:")
    env = os.getenv('ENVIRONMENT', 'development')
    debug = os.getenv('DEBUG', 'False')
    
    print(f"   Ambiente: {env}")
    print(f"   Debug: {debug}")
    
    if env == 'production':
        if debug == 'True':
            warnings.append("⚠️  DEBUG=True em produção! Deve ser False")
        
        if 'sqlite' in os.getenv('DATABASE_URL', '').lower():
            warnings.append("⚠️  SQLite em produção! Use PostgreSQL")
        
        if not os.getenv('SENTRY_DSN'):
            warnings.append("⚠️  Sentry não configurado em produção")
    
    # Verificar arquivos
    print("\n📁 Arquivos:")
    root_dir = Path.cwd()
    
    files_to_check = {
        '.env': 'Configuração de ambiente',
        '.gitignore': 'Ignorar arquivos sensíveis',
        'requirements.txt': 'Dependências Python',
    }
    
    for file, description in files_to_check.items():
        file_path = root_dir / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} não encontrado")
            issues.append(f"Criar arquivo: {file}")
    
    # Resultado final
    print("\n" + "=" * 60)
    if not issues and not warnings:
        print("✅ TUDO CERTO! Ambiente configurado corretamente.")
    else:
        if issues:
            print("❌ PROBLEMAS ENCONTRADOS:")
            for issue in issues:
                print(f"   • {issue}")
        
        if warnings:
            print("\n⚠️  AVISOS:")
            for warning in warnings:
                print(f"   • {warning}")
    
    print("=" * 60 + "\n")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = check_env_vars()
    exit(0 if success else 1)