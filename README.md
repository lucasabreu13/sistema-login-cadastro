# Sistema de Login e Cadastro

Este projeto implementa um sistema de login e cadastro usando Python e Tkinter. Ele também inclui uma funcionalidade de raspagem de dados de um site (Books to Scrape) e geração de relatórios em Excel.

## Funcionalidades
- **Login e Cadastro**:
  - Permite cadastrar usuários e armazená-los em um arquivo `usuarios.json`.
  - Verifica login com base nos usuários cadastrados.

- **Raspagem de Dados**:
  - Coleta informações de livros (título, preço e disponibilidade) do site [Books to Scrape](http://books.toscrape.com/).

- **Geração de Relatório**:
  - Exporta os dados raspados para um arquivo Excel (`relatorio_livros.xlsx`).

## Tecnologias Utilizadas
- **Python**
- **Tkinter** (Interface Gráfica)
- **Requests** e **BeautifulSoup** (Raspagem de Dados)
- **Pandas** (Manipulação e Geração de Excel)

## Como Executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-login-cadastro.git
   cd sistema-login-cadastro
