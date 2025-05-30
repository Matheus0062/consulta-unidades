from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import json

app = Flask(__name__)
app.secret_key = 'chave-secreta-supersegura'  # Necessário para sessões

# 🔐 Função para carregar os usuários a partir do JSON
def carregar_usuarios():
    caminho = os.path.join(os.path.dirname(__file__), 'usuarios.json')
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()  # ← Carrega os usuários dinamicamente

        if usuario in usuarios and usuarios[usuario] == senha:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        else:
            erro = "Usuário ou senha incorretos!"
            return render_template("login.html", erro=erro)

    return render_template("login.html")

@app.route("/consulta", methods=["GET", "POST"])
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))

    resultado = None

    if request.method == "POST":
        entrada = request.form["unidade"].strip().upper()
        caminho = os.path.join(os.path.dirname(__file__), "Suporte.xlsx")

        colunas = ["Cidade", "Nome da unidade", "Serial do DVR", "MAC da central do alarme", "Última preventiva realizada"]
        df = pd.read_excel(caminho, usecols=colunas)

        resultados = df[df["Nome da unidade"].str.upper().str.contains(entrada)]

        if len(resultados) == 1:
            resultado = [resultados.iloc[0].to_dict()]
        elif len(resultados) > 1:
            resultado = resultados.to_dict(orient="records")
        else:
            resultado = []

    return render_template("index.html", resultado=resultado, usuario=session["usuario"])

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
