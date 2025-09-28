from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import datetime

# --- 1. Configurações do MongoDB (AS SUAS CONFIGURAÇÕES CORRETAS) ---
# Seus dados de conexão
MONGO_URI = "  pegar dados no site mongo referente a user e banco de dados "
DATABASE_NAME = "aulasADS"
COLLECTION_NAME = "alunos"

# --- 2. Inicialização do Flask e Conexão ao MongoDB ---
app = Flask(__name__)
client = None
db = None
collection = None

try:
    # Tenta conectar ao MongoDB Atlas uma única vez
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print(f"Flask conectado ao MongoDB Atlas no database '{DATABASE_NAME}' com sucesso!")

except ConnectionFailure as e:
    print(f"ERRO DE CONEXÃO COM O MONGODB: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado na inicialização: {e}")
    
# --- 3. Rota para exibir o formulário HTML ---
@app.route('/')
def index():
    # Renderiza o arquivo index.html (que está na pasta 'templates')
    return render_template('index.html')

# --- 4. Rota para receber os dados do formulário (POST) ---
@app.route('/submit', methods=['POST'])
def submit_aluno():
    # CORREÇÃO: PyMongo exige comparação com None
    if collection is None: 
        # Se a conexão falhou, retorna erro
        return render_template('index.html', message="Erro: Conexão com MongoDB falhou na inicialização."), 500

    try:
        # Pega os dados que vieram do formulário HTML
        nome = request.form['nome']
        matricula = request.form['matricula']
        curso = request.form['curso']
        
        # Cria o documento MongoDB com os dados do formulário
        novo_aluno = {
            "nome": nome,
            "matricula": matricula,
            "curso": curso,
            "data_cadastro": datetime.datetime.now(),
            "origem": "cadastro_web"
        }
        
        # Insere o documento na coleção 'alunos'
        collection.insert_one(novo_aluno)
        
        # Retorna para a página inicial, mostrando uma mensagem de sucesso
        return render_template('index.html', message=f"Aluno '{nome}' cadastrado com sucesso!")

    except Exception as e:
        # Se houver erro na inserção (ex: conexão perdida), retorna o erro
        return render_template('index.html', message=f"Erro ao inserir dados: {e}"), 500

# --- 5. Execução do Servidor ---
if __name__ == '__main__':
    # Roda o servidor Flask. debug=True reinicia automaticamente ao salvar.

    app.run(debug=True)
