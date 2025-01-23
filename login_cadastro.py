import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os

# Funções para gerenciamento de usuários
def carregar_usuarios():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as file:
            return json.load(file)
    return {}

def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as file:
        json.dump(usuarios, file, indent=4)

def realizar_cadastro(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        messagebox.showerror("Erro", "Usuário já existe! Tente outro nome.")
        return False

    usuarios[usuario] = senha
    salvar_usuarios(usuarios)
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    return True

def realizar_login(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios and usuarios[usuario] == senha:
        return True
    return False

# Função para exibir a tela principal
def mostrar_tela_principal():
    def raspar_dados_books_to_scrape(text_widget):
        try:
            # URL do site
            url = "http://books.toscrape.com/catalogue/page-1.html"
            livros = []  # Lista para armazenar os dados

            while url:
                # Fazendo a requisição para a página
                response = requests.get(url)
                response.raise_for_status()

                # Processando o HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # Encontrando os livros na página
                itens = soup.find_all('article', class_='product_pod')
                for item in itens:
                    titulo = item.find('h3').a['title']
                    preco = item.find('p', class_='price_color').get_text(strip=True)
                    estoque = item.find('p', class_='instock availability').get_text(strip=True)

                    livros.append({
                        "Título": titulo,
                        "Preço": preco,
                        "Disponibilidade": estoque
                    })

                # Verificando o link para a próxima página
                next_page = soup.find('li', class_='next')
                url = f"http://books.toscrape.com/catalogue/{next_page.a['href']}" if next_page else None

            # Adicionar os resultados ao widget de texto
            text_widget.delete(1.0, tk.END)
            for livro in livros:
                text_widget.insert(tk.END, f"Título: {livro['Título']}\nPreço: {livro['Preço']}\nDisponibilidade: {livro['Disponibilidade']}\n\n")

            return livros

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao acessar o site: {e}")
            return []

    def gerar_relatorio_excel(dados):
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para salvar. Execute a raspagem primeiro.")
            return

        df = pd.DataFrame(dados)
        arquivo = "relatorio_livros.xlsx"
        df.to_excel(arquivo, index=False)
        messagebox.showinfo("Sucesso", f"Relatório salvo como {arquivo}!")

    janela_principal = tk.Tk()
    janela_principal.title("Raspador de Dados de Livros")
    janela_principal.geometry("800x600")

    dados = []  # Lista para armazenar os dados raspados

    # Rótulo
    label = tk.Label(janela_principal, text="Raspagem de Dados de Livros", font=("Arial", 16))
    label.pack(pady=10)

    # Campo de texto para exibir os resultados
    text_widget = scrolledtext.ScrolledText(janela_principal, wrap=tk.WORD, width=90, height=25, font=("Arial", 10))
    text_widget.pack(pady=10)

    # Botão para raspar dados
    botao_raspar = tk.Button(janela_principal, text="Raspar Dados", font=("Arial", 14), bg="lightblue", command=lambda: raspar_dados_books_to_scrape(text_widget))
    botao_raspar.pack(pady=10)

    # Botão para gerar relatório em Excel
    botao_relatorio = tk.Button(janela_principal, text="Gerar Relatório Excel", font=("Arial", 14), bg="lightgreen", command=lambda: gerar_relatorio_excel(dados))
    botao_relatorio.pack(pady=10)

    janela_principal.mainloop()

# Função para exibir a tela de login e cadastro
def criar_tela_login():
    def realizar_login_clicado():
        usuario = entrada_usuario.get()
        senha = entrada_senha.get()
        if realizar_login(usuario, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            janela.destroy()
            mostrar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def realizar_cadastro_clicado():
        usuario = entrada_usuario.get()
        senha = entrada_senha.get()
        if realizar_cadastro(usuario, senha):
            entrada_usuario.delete(0, tk.END)
            entrada_senha.delete(0, tk.END)

    janela = tk.Tk()
    janela.title("Login e Cadastro")
    janela.geometry("400x300")

    # Rótulo
    label = tk.Label(janela, text="Sistema de Login e Cadastro", font=("Arial", 16))
    label.pack(pady=10)

    # Campo de entrada para usuário
    tk.Label(janela, text="Usuário:", font=("Arial", 12)).pack(pady=5)
    entrada_usuario = tk.Entry(janela, font=("Arial", 12))
    entrada_usuario.pack(pady=5)

    # Campo de entrada para senha
    tk.Label(janela, text="Senha:", font=("Arial", 12)).pack(pady=5)
    entrada_senha = tk.Entry(janela, font=("Arial", 12), show="*")
    entrada_senha.pack(pady=5)

    # Botão de login
    botao_login = tk.Button(janela, text="Login", font=("Arial", 14), bg="lightblue", command=realizar_login_clicado)
    botao_login.pack(pady=10)

    # Botão de cadastro
    botao_cadastro = tk.Button(janela, text="Cadastrar", font=("Arial", 14), bg="lightgreen", command=realizar_cadastro_clicado)
    botao_cadastro.pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    criar_tela_login()

