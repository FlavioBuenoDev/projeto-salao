#!/bin/bash
# start-prod.sh
echo "🚀 Iniciando Ambiente de Produção com Docker..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado."
    exit 1
fi

# Carregar variáveis de ambiente de produção
if [ -f .env.prod ]; then
    echo "📁 Carregando variáveis de ambiente de produção..."
    export $(cat .env.prod | xargs)
else
    echo "❌ Arquivo .env.prod não encontrado."
    exit 1
fi

# Build e iniciar os containers
echo "🔨 Construindo e iniciando containers de produção..."
docker-compose -f docker-compose.prod.yml up --build -d

echo "✅ Ambiente de produção iniciado!"
echo "🌐 Aplicação: http://localhost"
echo "🔙 API: http://localhost:8000"