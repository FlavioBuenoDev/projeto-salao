
# Projeto Salão

Sistema completo para gestão de salão de beleza, com backend em FastAPI (Python) e frontend em React + Vite.

## Estrutura

- **backend/**: API REST com FastAPI, SQLModel, autenticação JWT, relatórios, integração com email.
- **frontend/**: Interface web moderna com React, Vite, MUI, gráficos e autenticação.

## Como rodar localmente

### Pré-requisitos
- Docker e Docker Compose instalados (recomendado)
- Python 3.11+ (opcional para rodar backend sem Docker)
- Node.js 18+ (opcional para rodar frontend sem Docker)

### Backend (FastAPI)
```bash
cd backend
# Instale dependências (opcional)
pip install -r requirements.txt
# Execute localmente
uvicorn app.main:app --reload
# Ou rode testes
pytest
```

### Frontend (React)
```bash
cd frontend
# Instale dependências
npm install
# Execute em modo dev
npm run dev
# Build para produção
npm run build
# Testes de lint/format
npm run lint
npm run format
```

## Usando Docker

### Backend produção
```bash
cd backend
docker build -f Dockerfile.prod -t salao-backend-prod .
docker run -p 8000:8000 salao-backend-prod
```

### Frontend produção
```bash
cd frontend
docker build -f Dockerfile.prod -t salao-frontend-prod .
docker run -p 80:80 salao-frontend-prod
```

### Docker Compose (dev ou prod)
```bash
docker-compose up --build
# Para produção use: docker-compose -f docker-compose.prod.yml up --build
```

## Variáveis de ambiente
- Configure o arquivo `.env` no backend para credenciais, segredos e configurações.
- Configure o arquivo `nginx.conf` no frontend para rotas e proxy se necessário.

## Testes
- Backend: `pytest backend/tests/`
- Frontend: `npm run lint` e `npm run format`

## Relatórios e exportação
- O backend gera relatórios em PDF e gráficos via endpoints protegidos.
- O frontend permite exportar dados e visualizar métricas em tempo real.

## Contato e suporte
Para dúvidas, sugestões ou problemas, abra uma issue ou entre em contato com o mantenedor.
