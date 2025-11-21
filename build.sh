#!/usr/bin/env bash
# exit on error
set -o errexit

echo "========================================="
echo "Iniciando build..."
echo "========================================="

# 1. Ir para a pasta do frontend e construir
echo "📦 Instalando e construindo Frontend..."
cd frontend
npm install
npm run build

# 2. O PULO DO GATO: Voltar para a raiz do projeto
# O erro aconteceu porque o script continuava dentro da pasta 'frontend'
cd ..

# 3. Instalar dependências do Python
# O comando abaixo assume que o requirements.txt está na RAÍZ (junto com o build.sh)
echo "📦 Instalando dependências do backend..."
pip install -r requirements.txt

echo "✅ Build finalizado com sucesso!"