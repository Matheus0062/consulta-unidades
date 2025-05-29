from flask import Flask, render_template, request 
import pandas as pd
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        entrada = request.form["unidade"].strip().upper()

        caminho = os.path.join(os.path.dirname(__file__), "Suporte.xlsx")
        colunas = ["Cidade", "Nome da unidade", "Serial do DVR", "MAC da central do alarme", "Última preventiva realizada"]
        df = pd.read_excel(caminho, usecols=colunas)
        print(df.columns)  # <-- Agora está na indentação certa

        resultados = df[df["Nome da unidade"].str.upper().str.contains(entrada)]

        if len(resultados) == 1:
            resultado = [resultados.iloc[0].to_dict()]  # ✅ sempre uma lista
        elif len(resultados) > 1:
            resultado = resultados.to_dict(orient="records")
        else:
            resultado = []  # ✅ lista vazia para HTML iterar

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
