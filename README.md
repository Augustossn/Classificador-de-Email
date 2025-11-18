## Classificador Inteligente de Emails com IA

Uma aplicação web simples que classifica automaticamente emails como Produtivo ou Improdutivo e sugere respostas automáticas usando Inteligência Artificial.

# Funcionalidades

Classificação Automática - Categoriza emails em Produtivo ou Improdutivo
Processamento de Texto (NLP) - Limpeza e análise inteligente de texto
Geração de Respostas - Sugere respostas automáticas contextualizadas
Upload de Arquivos - Suporta .txt e .pdf
Interface Moderna - Design responsivo com React
API REST - Backend em Python com Flask

# Tecnologias

Camada
Tecnologia
Frontend
React 18 + Axios
Backend
Flask (Python)
NLP
NLTK (Natural Language Toolkit)
IA
OpenAI API (GPT-3.5)
Deploy
Render.com


# Pré-requisitos

•
Node.js 14+ (para frontend)

•
Python 3.8+ (para backend)

•
npm ou yarn (gerenciador de pacotes)

•
pip (gerenciador de pacotes Python)

•
Chave da OpenAI API ou AI Studio

# Instalação Local

Clonar o Repositório

Bash


git clone <seu-repositorio>
cd email_classifier_simple


Configurar Backend (Python)

Bash


# Entrar na pasta do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env

# Editar .env e adicionar sua chave OpenAI
# OPENAI_API_KEY=sua_chave_aqui


Configurar Frontend (React)

Bash


# Voltar para a pasta raiz
cd ../frontend

# Instalar dependências
npm install

# Criar arquivo .env
cp .env.example .env

# Editar .env (se necessário)
# REACT_APP_API_URL=http://localhost:5000


Executar Localmente

Terminal 1 - Backend

Bash


cd backend
source venv/bin/activate  # ou venv\Scripts\activate no Windows
python app.py


O backend estará em: http://localhost:5000

Terminal 2 - Frontend

Bash


cd frontend
npm start


O frontend estará em: http://localhost:3000

Como Usar

1.
Abra http://localhost:3000 no navegador

2.
Escolha uma opção:

•
Colar texto direto do email

•
Fazer upload de arquivo (.txt ou .pdf )



3.
Clique em "Classificar Email"

4.
Veja os resultados:

•
Categoria (Produtivo/Improdutivo)

•
Nível de confiança

•
Motivo da classificação

•
Resposta sugerida



5.
Copie a resposta sugerida com um clique

Endpoints da API

POST /classify

Classifica um email

Entrada (JSON):

JSON


{
  "email_content": "Olá, gostaria de saber o status da minha requisição..."
}


Entrada:

Plain Text


file: <arquivo .txt ou .pdf>


Saída:

JSON


{
  "sucesso": true,
  "categoria": "Produtivo",
  "confianca": "Alta",
  "motivo": "Email solicita ação específica (atualização de status)",
  "resposta_sugerida": "Obrigado por entrar em contato. Estamos verificando..."
}


GET /health

Verifica se a API está funcionando

Saída:

JSON


{
  "status": "ok",
  "message": "API funcionando"
}


GET /test

Testa a API com um email de exemplo

Exemplos de Classificação

Email Produtivo

Entrada:


Olá, gostaria de saber o status da minha requisição #12345 que foi aberta em 01/11/2025. Ainda não recebi retorno sobre o problema.

Resultado:

•
Categoria: Produtivo

•
Confiança: Alta

•
Motivo: Email solicita ação específica

•
Resposta: Obrigado por entrar em contato. Estamos verificando o status de sua requisição e você receberá uma atualização em breve.

Email Improdutivo

Entrada:


Feliz Natal! Desejo um ótimo fim de ano para você e sua equipe!

Resultado:

•
Categoria: Improdutivo

•
Confiança: Alta

•
Motivo: Mensagem de felicitação que não requer ação imediata

•
Resposta: Obrigado pelas felicitações! Desejamos um excelente ano novo para você também!

Deploy em Nuvem

Opção 1: Render.com

1.
Criar conta em https://render.com

2.
Fazer fork do repositório no GitHub

3.
Conectar Render.com com GitHub

4.
Criar serviço para o backend:

•
Build command: pip install -r requirements.txt

•
Start command: gunicorn app:app

•
Environment: Adicionar OPENAI_API_KEY



5.
Criar serviço para o frontend:

•
Build command: npm install && npm run build

•
Publish directory: build



Opção 2: Heroku

1.
Criar conta em https://www.heroku.com

2.
Instalar Heroku CLI

3.
Deploy backend:

4.
Deploy frontend:

Opção 3: Vercel

1.
Criar conta em https://vercel.com

2.
Importar repositório

3.
Configurar variáveis de ambiente

4.
Deploy automático

Troubleshooting

Erro: "Falha ao conectar com o servidor"

Solução:

•
Verifique se o backend está rodando (http://localhost:5000/health )

•
Verifique se a URL da API está correta no .env do frontend

•
Verifique CORS no backend

Erro: "Invalid API Key"

Solução:

•
Verifique se a chave OpenAI está correta no .env

•
Verifique se a chave tem permissões para usar GPT-3.5

Erro: "File too large"

Solução:

•
Limite de arquivo é 5MB

•
Comprima ou divida o arquivo em partes menores

Estrutura do Projeto

Plain Text


email_classifier_simple/
├── backend/
│   ├── app.py              # Aplicação Flask
│   ├── classifier.py       # Lógica de classificação
│   ├── requirements.txt    # Dependências Python
│   ├── .env.example        # Exemplo de variáveis
│   └── uploads/            # Pasta para arquivos temporários
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── EmailForm.jsx
│   │   │   └── ResultDisplay.jsx
│   │   ├── styles/
│   │   │   ├── EmailForm.css
│   │   │   └── ResultDisplay.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
└── README.md


Segurança

•
Chaves de API: Nunca commit .env com chaves reais

•
CORS: Configurado para aceitar requisições do frontend

•
Validação: Todos os inputs são validados

•
Limite de arquivo: Máximo 5MB

Suporte

Para dúvidas ou problemas:

1.
Consulte a documentação da OpenAI: https://platform.openai.com/docs

2.
Consulte a documentação do Flask: https://flask.palletsprojects.com

3.
Consulte a documentação do React: https://react.dev

Licença

Este projeto é de código aberto e disponível sob a licença MIT.

