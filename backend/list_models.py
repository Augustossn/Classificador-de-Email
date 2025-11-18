import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("GOOGLE_API_KEY não foi encontrada em .env")
    exit(1)

print("Listando modelos disponíveis: \n")

try:
    for model in genai.list_models():
        print(f"{model.name}")
        print(f"Mostrar nomes: {model.display_name}")
        print(f"Métodos suportados: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"Erro ao listar modelos: {e}")
