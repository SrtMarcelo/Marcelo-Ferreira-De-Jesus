from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) # Vital para o site falar com o Python

def banco_dados():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mechanics", # Sua senha corrigida
        database="jotta_store" # Seu banco de dados
    )

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email_site = dados.get('email')
    senha_site = dados.get('senha')

    try:
        db = banco_dados()
        cursor = db.cursor(dictionary=True)
        
        # O segredo: use nomes de colunas que existem no seu banco.
        # Se sua tabela não chamar 'usuarios', mude o nome abaixo:
        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(query, (email_site, senha_site))
        resultado = cursor.fetchone()

        cursor.close()
        db.close()

        if resultado:
            return jsonify({"status": "sucesso", "mensagem": "Login efetuado com sucesso!"})
        else:
            return jsonify({"status": "erro", "mensagem": "Usuário ou senha inválidos."}), 401

    except Exception as e:
        # Isso imprimirá o erro exato no terminal do VS Code para você ler
        print(f"ERRO NO BANCO: {e}") 
        return jsonify({"status": "erro", "mensagem": f"Erro interno: {str(e)}"}), 500