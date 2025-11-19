# Classificador Inteligente de Emails com IA

Uma aplicação web simples que classifica automaticamente emails como Produtivo ou Improdutivo e sugere respostas automáticas usando Inteligência Artificial.

---

## Funcionalidades

* Classificação automática de emails
* Processamento de texto (NLP) com NLTK
* Geração de respostas automáticas contextualizadas
* Suporte a upload de arquivos (.txt e .pdf)
* Interface moderna em React
* API REST com backend em Flask (Python)

---

## Tecnologias Utilizadas

| Camada   | Tecnologia           |
| -------- | -------------------- |
| Frontend | React 18 + Axios     |
| Backend  | Flask (Python)       |
| NLP      | NLTK                 |
| IA       | OpenAI API (GPT-3.5) |
| Deploy   | Render.com           |

---

## Pré-requisitos

* Node.js 14+
* Python 3.8+
* npm ou yarn
* pip
* Chave da OpenAI API ou AI Studio

---

## Instalação Local

### 1. Clonar o Repositório

```bash
git clone https://github.com/Augustossn/Classificador-de-Email
cd Classificador de email
```

---

### 2. Configurar Backend (Python)

```bash
cd backend
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
```

Adicionar ao `.env`:

```
GOOGLE_API_KEY=sua_chave_aqui
```

---

### 3. Configurar Frontend (React)

```bash
cd ../frontend
npm install
cp .env.example .env
```

Se necessário, editar:

```
REACT_APP_API_URL=http://localhost:5000
```

---

## Execução Local

### Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate
python app.py
```

Backend em: [http://localhost:5000](http://localhost:5000)

### Frontend (Terminal 2)

```bash
cd frontend
npm start
```

Frontend em: [http://localhost:3000](http://localhost:3000)

---

## Como Usar

1. Acesse [http://localhost:3000](http://localhost:3000)
2. Cole o texto do email ou envie um arquivo .txt / .pdf
3. Clique em "Classificar Email"
4. Visualize categoria, confiança, motivo e resposta sugerida
5. Copie a resposta com um clique

---

## Endpoints da API

### POST /classify

Entrada JSON:

```json
{
  "email_content": "Olá, gostaria de saber o status da minha requisição..."
}
```

Entrada por arquivo:

```
file: <arquivo .txt ou .pdf>
```

Exemplo de resposta:

```json
{
  "sucesso": true,
  "categoria": "Produtivo",
  "confianca": "Alta",
  "motivo": "Email solicita ação específica (atualização de status)",
  "resposta_sugerida": "Obrigado por entrar em contato. Estamos verificando..."
}
```

---

### GET /health

```json
{
  "status": "ok",
  "message": "API funcionando"
}
```

### GET /test

Retorna um email de teste classificado.

---

## Exemplos de Classificação

### Email Produtivo

Entrada:

> Olá, gostaria de saber o status da minha requisição #12345 que foi aberta em 01/11/2025.

Resultado:

* Categoria: Produtivo
* Confiança: Alta
* Motivo: Solicita ação específica
* Resposta: "Obrigado por entrar em contato. Estamos verificando o status..."

---

### Email Improdutivo

Entrada:

> Feliz Natal! Desejo um ótimo fim de ano para você e sua equipe!

Resultado:

* Categoria: Improdutivo
* Confiança: Alta
* Motivo: Mensagem sem necessidade de ação
* Resposta: "Obrigado pelas felicitações..."

---

## Deploy em Nuvem

### Render.com

1. Criar conta no Render
2. Fazer fork do repositório
3. Conectar GitHub ao Render
4. Criar serviço do backend:

   * Build: `pip install -r requirements.txt`
   * Start: `gunicorn app:app`
   * Variáveis: `OPENAI_API_KEY`
5. Criar serviço do frontend:

   * Build: `npm install && npm run build`
   * Publish directory: `build`

### Heroku

* Criar conta
* Instalar CLI
* Deploy do backend
* Deploy do frontend

### Vercel

* Criar conta
* Importar repositório
* Configurar variáveis de ambiente
* Deploy automático

---

## Problemas Comuns (Troubleshooting)

### Erro: "Falha ao conectar com o servidor"

* Verifique backend ([http://localhost:5000/health](http://localhost:5000/health))
* Confirme URL da API
* Verifique CORS

### Erro: "Invalid API Key"

* Cheque chave no .env
* Confirme permissões da chave

### Erro: "File too large"

* Limite máximo: 5MB
* Comprima ou divida o arquivo

---

## Estrutura do Projeto

```
email_classifier_simple/
├── backend/
│   ├── app.py
│   ├── classifier.py
│   ├── requirements.txt
│   ├── .env.example
│   └── uploads/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
└── README.md
```

---

## Segurança

* Não faça commit de chaves reais
* CORS configurado apenas para o frontend
* Inputs validados
* Limite de upload de 5MB

---

## Suporte

* Documentação AIStudio: [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)
* Documentação Flask: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
* Documentação React: [https://react.dev](https://react.dev)

---

## Licença

Este projeto é de código aberto e disponível sob a licença MIT.
