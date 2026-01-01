

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) # Isso permite que o HTML fale com o Python

def banco_dados():
    return mysql.connector.connect(
        host="trolley.proxy.rlwy.net",
        user="root",
        password="EeNteZTbajQvwuSPvWFNZAQUDzNmKPsK",
        database="railway",
        port=53280
    )

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
        return jsonify({"mensagem": "Login efetuado com sucesso!"}), 200
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
    

