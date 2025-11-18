import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
from dotenv import load_dotenv
from classifier import EmailClassifier

load_dotenv()

app = Flask(__name__)
CORS(app)  

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'} # formatos permitidos
MAX_FILE_SIZE = 5 * 1024 * 1024  # tamanho máximo

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

classifier = EmailClassifier()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file_path):
    # extração de texto do arquivo pdf ou txt
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_path.endswith('.pdf'):
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        
        return ""
    
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo: {str(e)}")


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "API funcionando"}), 200


@app.route('/classify', methods=['POST'])
def classify():
    # classifição de email
    try:
        email_content = None
        
        # opção de colar o email
        if request.is_json:
            data = request.get_json()
            email_content = data.get('email_content', '').strip()
        
        # opção de upar o email
        elif 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({"sucesso": False, "erro": "Nenhum arquivo selecionado"}), 400
            
            if not allowed_file(file.filename):
                return jsonify({"sucesso": False, "erro": "Arquivo deve ser .txt ou .pdf"}), 400
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            email_content = extract_text_from_file(file_path)
            
            os.remove(file_path)
        
        if not email_content:
            return jsonify({"sucesso": False, "erro": "Email vazio ou não fornecido"}), 400
        
        resultado = classifier.process_email(email_content)
        
        return jsonify(resultado), 200 if resultado.get("sucesso") else 400
    
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": f"Erro no servidor: {str(e)}"
        }), 500


@app.route('/test', methods=['GET'])
def test():
    # teste para ver se API está funcionando corretamente
    email_teste = """
    Olá,
    
    Gostaria de saber o status da minha requisição #12345 que foi aberta em 01/11/2025.
    Ainda não recebi retorno sobre o problema.
    
    Obrigado,
    Cliente
    """
    
    resultado = classifier.process_email(email_teste)
    return jsonify(resultado), 200


@app.errorhandler(404) # erro nas rotas
def not_found(error):
    return jsonify({"erro": "Rota não encontrada"}), 404


@app.errorhandler(500) # erro interno
def internal_error(error):
    return jsonify({"erro": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
