import os
import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") # arrumar chave no .env 
if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("GOOGLE_API_KEY não foi encontrada em .env")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class EmailClassifier:
    
    def __init__(self):
        self.stemmer = SnowballStemmer('portuguese')
        self.stop_words = set(stopwords.words('portuguese'))
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite') # para usar outros modelos disponíveis, digita no terminal "python list_models.py"
        
    def preprocess_text(self, text):
        text = text.lower() 
        
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE ) # remove URLs
        
        text = re.sub(r'\S+@\S+', '', text) # remove emails
        
        text = re.sub(r'[^a-záéíóúâêôãõç\s]', '', text) # remove pontuções e caracteres especiais
        
        tokens = word_tokenize(text)
        
        # removedor de stopwords e utiliza stemming para agrupar palavras
        processed_tokens = [
            self.stemmer.stem(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        
        return ' '.join(processed_tokens)
    
    def classify_email(self, email_content):

        try:
            processed_text = self.preprocess_text(email_content)
        
            # texto feito por ia para fazer um bom prompt, caso queira mudar o resultado ou melhorar, mude esse prompt
            prompt = f"""Você é um classificador de emails. Classifique o email em uma das duas categorias:

            PRODUTIVO: Emails que requerem ação ou resposta específica (solicitações de suporte, atualização sobre casos, dúvidas sobre sistema, etc.)
            IMPRODUTIVO: Emails que não necessitam de ação imediata (felicitações, agradecimentos, mensagens não relevantes, etc.)

            Responda APENAS com um JSON válido neste formato exato:
            {{
                "categoria": "Produtivo" ou "Improdutivo",
                "confianca": "Alta", "Média" ou "Baixa",
                "motivo": "Explicação breve da classificação"
            }}

            Email para classificar:
            {email_content}"""
            
            # chama a API
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # remove md
            if '```' in result_text:
                parts = result_text.split('```')
                for part in parts:
                    if '{' in part:
                        result_text = part.strip()
                        if result_text.startswith('json'):
                            result_text = result_text[4:].strip()
                        break
            
            result = json.loads(result_text)
            
            return {
                "sucesso": True,
                "categoria": result.get("categoria", "Desconhecido"),
                "confianca": result.get("confianca", "Baixa"),
                "motivo": result.get("motivo", "")
            }
            
        except json.JSONDecodeError as e:
            return {
                "sucesso": False,
                "erro": f"Erro ao parsear resposta JSON: {str(e)}"
            }
        except Exception as e:
            return {
                "sucesso": False,
                "erro": f"Erro na classificação: {str(e)}"
            }
    
    def generate_response(self, email_content, categoria):
        
        # resposta automática com base na classificação do email
        try:
            if categoria == "Produtivo":
                # mude o prompt aqui caso queira melhorar a resposta
                prompt = f"""Gere uma resposta profissional, concisa e educada para este email de suporte/solicitação:

                {email_content}

                A resposta deve:
                - Ser breve (2-3 linhas)
                - Manter tom profissional
                - Indicar que a solicitação será atendida
                - Ser genérica o suficiente para qualquer email produtivo

                Responda APENAS com a resposta, sem explicações adicionais."""
            else:
                prompt = f"""Gere uma resposta breve e educada para este email de felicitação/agradecimento:

                {email_content}

                A resposta deve:
                - Ser breve (1-2 linhas)
                - Manter tom profissional e amigável
                - Agradecer a mensagem
                - Ser genérica o suficiente para qualquer email improdutivo

                Responda APENAS com a resposta, sem explicações adicionais."""
                            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"
    
    def process_email(self, email_content):
        
        if not email_content or len(email_content.strip()) < 10:
            return {
                "sucesso": False,
                "erro": "Email deve ter pelo menos 10 caracteres"
            }
        
        classificacao = self.classify_email(email_content)
        
        if not classificacao.get("sucesso"):
            return classificacao
        
        resposta = self.generate_response(
            email_content,
            classificacao.get("categoria")
        )
        
        return {
            "sucesso": True,
            "categoria": classificacao.get("categoria"),
            "confianca": classificacao.get("confianca"),
            "motivo": classificacao.get("motivo"),
            "resposta_sugerida": resposta
        }
