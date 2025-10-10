# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o código da aplicação
COPY . .

# Expor a porta que a aplicação roda
EXPOSE 5173

# Comando para rodar a aplicação
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]