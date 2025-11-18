#!/bin/bash
set -e  # Parar se houver erro

echo "========================================="
echo "Iniciando build..."
echo "========================================="

# Frontend
echo ""
echo "📦 Instalando dependências do frontend..."
cd frontend
npm install --legacy-peer-deps
echo "🏗️  Fazendo build do frontend..."
npm run build
echo "✅ Frontend build completo!"
cd ..

# Backend
echo ""
echo "📦 Instalando dependências do backend..."
cd backend
pip install -r requirements.txt
echo "✅ Backend dependências instaladas!"
cd ..

echo ""
echo "========================================="
echo "✅ Build completo com sucesso!"
echo "========================================="
