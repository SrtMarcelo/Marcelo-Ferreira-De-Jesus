from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Sua função de conexão que você já domina
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Banco-lite" # O nome que aparece no seu DB
    )

@app.route('/')
def login_page():
    # Primeira coisa que o usuário vê ao abrir 127.0.0.1:5000
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def verificar_login():
    usuario_input = request.form.get('usuario')
    senha_input = request.form.get('senha')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # A query para verificar o e-mail
    query = "SELECT * FROM people WHERE nome = %s AND email = %s"
    cursor.execute(query, (usuario_input, senha_input))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        # SE ACERTAR: Ele pula para a rota do site principal...
        return redirect(url_for('abrir_site'))
    else:
        return "Dados inválidos. Tente novamente."

@app.route('/meu-site-principal')
def abrir_site():
    # Entrega o site que já tinha 
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)