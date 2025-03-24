import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Conectar ao MongoDB
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = client["user_crud_db"]
collection = db["users"]

# Limpar a coleção existente
collection.delete_many({})

# Ler o arquivo users.json
try:
    with open("users.json", "r") as file:
        data = json.load(file)
except json.JSONDecodeError as e:
    print(f"Erro ao ler o users.json: {e}")
    exit(1)
except FileNotFoundError:
    print("Arquivo users.json não encontrado.")
    exit(1)

# Acessar a lista de usuários dentro da chave "users"
if "users" not in data:
    print("O arquivo users.json deve conter uma chave 'users' com uma lista de usuários.")
    exit(1)

users_data = data["users"]

# Garantir que users_data é uma lista
if not isinstance(users_data, list):
    print(f"Formato inesperado para 'users': {type(users_data)}. Esperava-se uma lista.")
    exit(1)

# Transformar os dados para o formato esperado
users = []
for user in users_data:
    # Mapear os campos do users.json para o formato esperado
    roles = []
    if user.get("is_user_admin"):
        roles.append("admin")
    if user.get("is_user_manager"):
        roles.append("manager")
    if user.get("is_user_tester"):
        roles.append("tester")

    # Converter created_at (ISO 8601) para timestamp Unix
    created_at = datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    created_ts = int(created_at.timestamp())

    # Criar o documento no formato esperado
    transformed_user = {
        "username": user["user"],
        "password": user["password"],
        "roles": roles,
        "preferences": {
            "timezone": user["user_timezone"]
        },
        "active": user["is_user_active"],
        "created_ts": created_ts
    }
    users.append(transformed_user)

# Inserir os usuários no MongoDB
for user in users:
    try:
        collection.insert_one(user)
    except Exception as e:
        print(f"Erro ao inserir usuário {user.get('username', 'desconhecido')}: {e}")

print(f"Inseridos {collection.count_documents({})} usuários no MongoDB.")