# Mini Projeto 3 - Consumo de APIs

Projeto para a disciplina de Linguagem de Programação 2.

## Estrutura
- **Server**: API em FastAPI responsável por traduzir textos e salvar o histórico em memória.
- **Client**: Script em Python para consumir a API.

## Como rodar o servidor
1. Instale as dependências: `pip install -r requirements.txt`
2. Rode: `uvicorn server.main:app --reload`
3. Acesse a documentação: `http://127.0.0.1:8000/docs`