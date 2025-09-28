from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# --- 1. Sua String de Conexão ---
# PROFESSOR, SUBSTITUA ESTA STRING COM A QUE VOCÊ COPICOU DO ATLAS!
# Não se esqueça de substituir <username> e <password> pelos seus reais!
# USE ESTA STRING CORRIGIDA:
MONGO_URI = "pegar no site mongo "

# --- 2. Nome do Database e da Collection que você criou ---
DATABASE_NAME = "aulasADS"
COLLECTION_NAME = "alunos"

def inserir_documentos_alunos():
    client = None # Inicializa client como None para garantir que seja fechado
    try:
        # Conecta ao MongoDB Atlas
        print(f"Conectando ao MongoDB Atlas no database '{DATABASE_NAME}'...")
        client = MongoClient(MONGO_URI)
        
        # O comando client.admin.command('ping') é útil para verificar a conexão
        client.admin.command('ping')
        print("Conexão estabelecida com sucesso!")
        
        # Seleciona o database e a collection
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # --- 3. Documentos de exemplo para inserir ---
        documento_aluno_1 = {
            "nome": "Ana Silva",
            "matricula": "2023001",
            "curso": "Análise e Desenvolvimento de Sistemas",
            "fase": 5,
            "disciplinas_atuais": ["Banco de Dados II", "Programação Web"],
            "contato": {
                "email": "ana.silva@aluno.fmp.br",
                "telefone": "48987654321"
            },
            "notas": [
                {"disciplina": "Banco de Dados II", "nota": 8.5},
                {"disciplina": "Programação Web", "nota": 9.0}
            ]
        }
        documento_aluno_2 = {
            "nome": "Bruno Mendes",
            "matricula": "2023002",
            "curso": "Análise e Desenvolvimento de Sistemas",
            "fase": 5,
            "disciplinas_atuais": ["Banco de Dados II", "Engenharia de Software"],
            "contato": {
                "email": "bruno.mendes@aluno.fmp.br",
                "telefone": "48991234567"
            },
            "observacoes": "Participa ativamente das aulas."
        }

        documentos_alunos_novos = [
            {
                "nome": "Carla Oliveira",
                "matricula": "2023003",
                "curso": "Análise e Desenvolvimento de Sistemas",
                "fase": 5,
                "contato": {"email": "carla.ol@aluno.fmp.br"}
            },
            {
                "nome": "Daniel Costa",
                "matricula": "2023004",
                "curso": "Análise e Desenvolvimento de Sistemas",
                "fase": 5,
                "disciplinas_atuais": ["Banco de Dados II"]
            }
        ]
        
        # --- 4. Inserir um único documento ---
        print(f"\nInserindo um documento de aluno na coleção '{COLLECTION_NAME}'...")
        resultado_um = collection.insert_one(documento_aluno_1)
        print(f"Documento inserido com _id: {resultado_um.inserted_id}")
        
        # --- 5. Inserir múltiplos documentos ---
        print(f"\nInserindo múltiplos documentos de alunos na coleção '{COLLECTION_NAME}'...")
        resultado_varios = collection.insert_many(documentos_alunos_novos)
        print(f"Documentos inseridos com _ids: {resultado_varios.inserted_ids}")

        # --- 6. Inserir outro documento para demonstrar flexibilidade de esquema ---
        print(f"\nInserindo um segundo documento de aluno (com campos diferentes)...")
        resultado_dois = collection.insert_one(documento_aluno_2)
        print(f"Documento inserido com _id: {resultado_dois.inserted_id}")
        
        print("\nOperações de inserção concluídas com sucesso!")

    except ConnectionFailure as e:
        print(f"Erro de conexão com o MongoDB: {e}")
    except OperationFailure as e:
        print(f"Erro de operação no MongoDB: {e.details.get('errmsg', e)}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if client:
            print("Fechando conexão com o MongoDB.")
            client.close()

if __name__ == "__main__":

    inserir_documentos_alunos()
