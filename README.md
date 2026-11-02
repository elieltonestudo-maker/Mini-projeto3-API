# Mini Projeto 3 - Consumo de APIs

Projeto desenvolvido para a disciplina de Linguagem de Programação 2, do curso de Inteligência Artificial da Fatec Rio Claro - SP.

Professor: Orlando Saraiva Jr.

## Integrantes
- Elielton Barbosa (Responsável pelo Servidor API e Estrutura do projeto)
- Luiz Eduardo Azevedo (Responsável pelo Cliente Web e Terminal)

## Sobre o Projeto
O sistema é um tradutor inteligente que detecta o idioma de origem automaticamente (autodetecção) e traduz textos e arquivos PDF. 
- Servidor (Backend): API construída em FastAPI. Utiliza a biblioteca langdetect para descobrir o idioma de entrada e deep-translator (motor MyMemory) para realizar a tradução. Mantém um histórico em memória.
- Cliente (Frontend): Possui duas opções de uso:
  1. Interface Web (Streamlit) com abas para digitar texto ou fazer upload de PDF.
  2. Menu no Terminal (Python).

## Como executar o projeto

### 1. Clonar o repositório
Abra o seu terminal ou prompt de comando e clone o projeto:

git clone https://github.com/elieltonestudo-maker/Mini-projeto3-API.git
cd Mini-projeto3-API

### 2. Criar e Ativar o Ambiente Virtual (venv)
É altamente recomendado usar um ambiente virtual para não misturar as bibliotecas do projeto com as do sistema.

No Windows (PowerShell/CMD):
python -m venv venv
.\venv\Scripts\activate

No Linux/Mac:
python3 -m venv venv
source venv/bin/activate

(Você saberá que deu certo porque aparecerá (venv) no início da linha de comando).

### 3. Instalar as dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

pip install -r requirements.txt

### 4. Rodar o Projeto Completo (Método Rápido)
Criamos um script app.py que liga o servidor e a interface web ao mesmo tempo. Basta rodar:

python app.py

(O navegador abrirá automaticamente com a tela do tradutor web. Para encerrar, aperte Ctrl + C no terminal).

### 5. Rodar Manualmente (Separado)
Se preferir testar as partes separadamente, abra um terminal para o Servidor e OUTRO terminal (de sua escolha) para o Cliente.

Terminal 1 (Servidor - Obrigatório):
uvicorn server.main:app --reload
Acesse http://127.0.0.1:8000/docs para ver a documentação interativa da API.

Para o Terminal 2, escolha UMA das opções de cliente abaixo:

Opção A - Cliente via Terminal (Menu interativo):
python client/main.py

Opção B - Cliente via Web (Interface no navegador):
streamlit run client/app_web.py

## Limitações Conhecidas
- Limite de caracteres (MyMemory): O motor de tradução gratuito possui um limite de aproximadamente 500 caracteres por requisição. Para evitar erros, o sistema limita a leitura de PDFs e textos para 400 caracteres por vez.
- PDFs escaneados: A biblioteca PyPDF2 extrai apenas texto selecionável. Se o PDF for uma imagem escaneada, a extração falhará.
- Detecção de idioma: Frases muito curtas (1 ou 2 palavras) podem ser detectadas incorretamente pela biblioteca langdetect.