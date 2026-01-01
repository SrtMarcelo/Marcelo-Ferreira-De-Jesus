from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def banco_dados():
    # Esta é a forma correta: o return engloba toda a conexão
    return mysql.connector.connect(
        host="trolley.proxy.rlwy.net",
        user="root",
        password="EeNteZTbajQvwuSPvWFNZAQUDzNmKPsK",
        database="railway",
        port=53280
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    dados = request.form
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

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    
    dados = request.form
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
    app.run(host='0.0.0.0', port=5000)