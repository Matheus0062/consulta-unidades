import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
import unicodedata
import os

# Remove acentos e coloca tudo em caixa baixa
def normalizar(texto):
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('ASCII').lower()

# Leitura da planilha
try:
    colunas_desejadas = ['Cidade', 'Nome da unidade', 'Serial do DVR', 'MAC da central do alarme', 'Última preventiva realizada']
    df = pd.read_excel('Suporte.xlsx', usecols=colunas_desejadas)
    df['nome_normalizado'] = df['Nome da unidade'].apply(normalizar)
except FileNotFoundError:
    tk.Tk().withdraw()
    messagebox.showerror("Erro", "A planilha 'Suporte.xlsx' não foi encontrada.")
    raise

# Interface
def buscar_unidade():
    root = tk.Tk()
    root.withdraw()
    
    entrada = simpledialog.askstring("Buscar Unidade", "Digite o nome da unidade:")
    
    if not entrada:
        messagebox.showwarning("Entrada vazia", "Nenhum nome foi digitado.")
        return
    
    entrada_normalizada = normalizar(entrada)
    
    # Filtra por substring
    resultados = df[df['nome_normalizado'].str.contains(entrada_normalizada)]

    if resultados.empty:
        messagebox.showinfo("Não encontrado", "Unidade não localizada na planilha.")
    elif len(resultados) == 1:
        mostrar_resultado(resultados.iloc[0])
    else:
        # Múltiplos resultados - escolha
        opcoes = resultados['Nome da unidade'].tolist()
        escolha = simpledialog.askstring("Várias opções encontradas", f"Várias unidades encontradas:\n{chr(10).join(opcoes)}\n\nDigite o nome exato:")
        if escolha:
            escolha_normalizada = normalizar(escolha)
            filtro = resultados[resultados['nome_normalizado'] == escolha_normalizada]
            if not filtro.empty:
                mostrar_resultado(filtro.iloc[0])
            else:
                messagebox.showinfo("Erro", "Unidade não encontrada entre as opções listadas.")
        else:
            messagebox.showinfo("Cancelado", "Busca cancelada.")

def mostrar_resultado(linha):
    mensagem = (
        f"Cidade: {linha['Cidade']}\n"
        f"Nome da unidade: {linha['Nome da unidade']}\n"
        f"Serial do DVR: {linha['Serial do DVR']}\n"
        f"MAC da central do alarme: {linha['MAC da central do alarme']}\n"
        f"Última preventiva realizada: {linha['Última preventiva realizada']}"
    )
    messagebox.showinfo("Resultado encontrado", mensagem)

# Executar
buscar_unidade()
