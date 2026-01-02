from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Servidor Online! Use /login no seu navegador."

def banco_dados():
    DATABASE_URL = "postgresql://jotta_db_user:18bbKOHR2wUPOhmT1z3IDFcV7DrS86Nx@dpg-d59u69ali9vc73as2hq0-a.oregon-postgres.render.com/jotta_db"
    return psycopg2.connect(DATABASE_URL)

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

if __name__ == '__main__':
    app.run(debug=True)