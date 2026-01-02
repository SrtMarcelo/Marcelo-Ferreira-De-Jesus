from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# --- NOVA ROTA PARA RESOLVER O ERRO 404 (NOT FOUND) ---
@app.route('/')
def home():
    return "Servidor Online! Use /login para acessar."

# --- CONFIGURAÇÃO DO BANCO DE DADOS POSTGRESQL ---
def banco_dados():
    DATABASE_URL = "postgresql://jotta_db_user:l8bbKoHR2wUPohmT1z3IDFcV7DrS86Nx@dpg-d59u69ali9vc73as2hq0-a.oregon-postgres.render.com/jotta_db"
    return psycopg2.connect(DATABASE_URL)

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    conexao = banco_dados()
    cursor = conexao.cursor()
    # O PostgreSQL usa %s como marcador de posição
    cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
    usuario = cursor.fetchone()
    
    conexao.close()
    if usuario:
        return jsonify({"mensagem": "Login efetuado!"}), 200
    return jsonify({"erro": "Dados inválidos"}), 401

@app.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    conexao = banco_dados()
    cursor = conexao.cursor()
    try:
        sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, senha))
        conexao.commit()
        return jsonify({"mensagem": "Cadastrado!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conexao.close()

if __name__ == '__main__':
    app.run(debug=True)