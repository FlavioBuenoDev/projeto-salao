

# ==============================================================================
# ARQUIVO 3: backend/scripts/generate_secret_key.py
# ==============================================================================
"""
Script simples para gerar SECRET_KEY
Execute: python scripts/generate_secret_key.py
"""

import secrets

def generate_keys(count=3):
    """Gera múltiplas chaves seguras"""
    
    print("\n" + "=" * 60)
    print("🔑 GERADOR DE SECRET KEYS")
    print("=" * 60 + "\n")
    
    print("Copie uma destas chaves para seu .env:\n")
    
    for i in range(count):
        key = secrets.token_urlsafe(32)
        print(f"Opção {i+1}:")
        print(f"SECRET_KEY={key}\n")
    
    print("=" * 60)
    print("⚠️  IMPORTANTE:")
    print("   • Use chaves diferentes para dev e produção")
    print("   • NUNCA compartilhe suas chaves")
    print("   • NUNCA commite .env no Git")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    generate_keys()