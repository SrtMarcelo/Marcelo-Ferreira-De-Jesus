from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# --- FUNÇÃO PARA CONECTAR AO BANCO ---
def banco_dados():
    # Adicionamos o ?sslmode=require para o Render aceitar a conexão segura
   DATABASE_URL =" postgresql://jotta_db_user:l8bbKoHR2wUPohmT1z3IDFcV7DrS86Nx@dpg-d59u69ali9vc73as2hq0-a.oregon-postgres.render.com/jotta_db?sslmode=require"
   return psycopg2.connect(DATABASE_URL)

# --- CRIA A TABELA AUTOMATICAMENTE SE ELA NÃO EXISTIR ---
def criar_tabela():
    try:
        conexao = banco_dados()
        cursor = conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, email TEXT UNIQUE, senha TEXT)")
        conexao.commit()
        conexao.close()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")

# Chamar a criação da tabela ao iniciar o app
criar_tabela()

@app.route('/')
def home():
    return "Servidor Online! Use /login no seu navegador."

# --- ROTA DE LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    conexao = banco_dados()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
    usuario = cursor.fetchone()
    conexao.close()
    
    if usuario:
        return jsonify({"mensagem": "Login efetuado!"}), 200
    return jsonify({"erro": "Dados inválidos"}), 401

# --- ROTA DE CADASTRO ---
@app.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    try:
        conexao = banco_dados()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (email, senha))
        conexao.commit()
        conexao.close()
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": "E-mail já cadastrado ou erro no banco"}), 400

if __name__ == '__main__':
    app.run(debug=True)