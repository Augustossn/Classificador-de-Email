import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
from dotenv import load_dotenv
from classifier import EmailClassifier

load_dotenv()

FRONTEND_BUILD = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_BUILD, 'static'),
    static_url_path='/static',
    template_folder=FRONTEND_BUILD
)

CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):

    if path and path.startswith('static/'):
        return send_from_directory(app.static_folder, path[7:])
    
    if path and os.path.exists(os.path.join(FRONTEND_BUILD, path)):
        return send_from_directory(FRONTEND_BUILD, path)
    
    index_path = os.path.join(FRONTEND_BUILD, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_BUILD, 'index.html')
    
    return jsonify({"erro": "Frontend não encontrado. Certifique-se que npm run build foi executado"}), 404

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

classifier = EmailClassifier()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file_path):
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


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "API funcionando"}), 200


@app.route('/api/classify', methods=['POST'])
def classify():
    try:
        email_content = None
        
        if request.is_json:
            data = request.get_json()
            email_content = data.get('email_content', '').strip()
        
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


@app.route('/api/test', methods=['GET'])
def test():
    email_teste = """
    Olá,
    
    Gostaria de saber o status da minha requisição #12345 que foi aberta em 01/11/2025.
    Ainda não recebi retorno sobre o problema.
    
    Obrigado,
    Cliente
    """
    
    resultado = classifier.process_email(email_teste)
    return jsonify(resultado), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"erro": "Rota não encontrada"}), 404


@app.errorhandler(500)
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
