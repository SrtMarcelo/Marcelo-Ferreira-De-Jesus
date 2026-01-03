const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// Conexão usando a variável que o Railway fornece automaticamente
const db = mysql.createConnection(process.env.MYSQL_URL);

app.post('/cadastrar', (req, res) => {
    const { nome, email, senha } = req.body;
    const sql = "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)";
    
    db.query(sql, [nome, email, senha], (err, result) => {
        if (err) return res.status(500).send(err);
        res.send({ message: "Cadastrado com sucesso!" });
    });
});

app.listen(process.env.PORT || 3000, () => console.log("Servidor rodando!"));
async function finalizarCadastro() {
    const dados = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value
    };

    // Cole o link que você gerou aqui, com o /cadastrar no final
    const resposta = await fetch('https://marcelo-ferreira-de-jesus-production.up.railway.app/cadastrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();
    alert(resultado.message);
}