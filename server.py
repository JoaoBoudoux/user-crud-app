from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
from bson import ObjectId

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Conectar ao MongoDB
try:
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
    db = client["user_crud_db"]
    collection = db["users"]
    print("Conexão com MongoDB estabelecida com sucesso")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    exit(1)

# Helper para serializar ObjectId
def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

# Tratamento de erros global
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Erro no servidor: {str(e)}")
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

# CRUD Operations

# Create
@app.route("/users", methods=["POST"])
def create_user():
    print("Recebida requisição POST para /users")
    data = request.get_json()
    print(f"Dados recebidos: {data}")
    if not data or not all(key in data for key in ["username", "password", "roles", "preferences", "created_ts"]):
        print("Erro: Campos obrigatórios ausentes")
        return jsonify({"error": "Missing required fields"}), 400
    
    data["active"] = data.get("active", True)
    data["last_updated_at"] = int(datetime.now().timestamp())  # Adiciona last_updated_at
    try:
        result = collection.insert_one(data)
        print(f"Usuário criado com ID: {result.inserted_id}")
        return jsonify({"message": "User created", "id": str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return jsonify({"error": str(e)}), 500

# Read (All Users)
@app.route("/users", methods=["GET"])
def get_users():
    print("Recebida requisição GET para /users")
    try:
        users = list(collection.find())
        print(f"Usuários encontrados: {len(users)}")
        return jsonify([serialize_user(user) for user in users]), 200
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return jsonify({"error": str(e)}), 500

# Read (Single User)
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    print(f"Recebida requisição GET para user_id: {user_id}")
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            print("Erro: Usuário não encontrado")
            return jsonify({"error": "User not found"}), 404
        return jsonify(serialize_user(user)), 200
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return jsonify({"error": str(e)}), 500

# Update
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    print(f"Recebida requisição PUT para user_id: {user_id}")
    data = request.get_json()
    print(f"Dados recebidos: {data}")
    if not data:
        print("Erro: Nenhum dado fornecido")
        return jsonify({"error": "No data provided"}), 400
    
    # Adiciona ou atualiza o campo last_updated_at
    data["last_updated_at"] = int(datetime.now().timestamp())
    try:
        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        if result.matched_count == 0:
            print("Erro: Usuário não encontrado")
            return jsonify({"error": "User not found"}), 404
        print("Usuário atualizado com sucesso")
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return jsonify({"error": str(e)}), 500

# Delete
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    print(f"Recebida requisição DELETE para user_id: {user_id}")
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            print("Erro: Usuário não encontrado")
            return jsonify({"error": "User not found"}), 404
        print("Usuário deletado com sucesso")
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Iniciando o servidor Flask...")
    app.run(debug=True, port=5000)