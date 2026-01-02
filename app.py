from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import psycopg2
app = Flask(__name__)
CORS(app) # Isso permite que o HTML fale com o Python

def banco_dados():
  return mysql.connector.connect(
            host="trolley.proxy.rlwy.net",
            user="root",
            password="EeNteZTbajQvwuSPvWFNZAQUDzNmKPsK",
            database="jotta_store",
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
    
    import psycopg2
import os

# Esse link abaixo é o que você copiou do Render
DATABASE_URL = "postgresql://jotta_db_user:l8bbKoHR2wUPohmT1z3IDFcV7DrS86Nx@dpg-d59u69ali9vc73as2hq0-a.oregon-postgres.render.com/jotta_db"

conn = psycopg2.connect(DATABASE_URL)