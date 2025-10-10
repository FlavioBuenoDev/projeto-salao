#!/bin/bash
# start-dev.sh
echo "🚀 Iniciando Ambiente de Desenvolvimento com Docker..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose."
    exit 1
fi

# Carregar variáveis de ambiente
if [ -f .env ]; then
    echo "📁 Carregando variáveis de ambiente..."
    export $(cat .env | xargs)
else
    echo "⚠️  Arquivo .env não encontrado. Usando valores padrão."
fi

# Build e iniciar os containers
echo "🔨 Construindo e iniciando containers..."
docker-compose up --build

echo "✅ Ambiente iniciado!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔙 Backend: http://localhost:8000"
echo "📚 Documentação da API: http://localhost:8000/docs"