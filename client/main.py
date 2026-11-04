import requests
import os
from PyPDF2 import PdfReader

# Endereço onde o nosso servidor (API) está rodando
URL_BASE = "http://127.0.0.1:8000"

# Função que abre o arquivo PDF e extrai o texto de dentro dele
def ler_pdf(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto_completo = ""
        # Passa por cada página do PDF e junta o texto
        for pagina in leitor.pages:
            texto_completo += pagina.extract_text() + "\n"
        return texto_completo.strip()
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None

# Função principal que mostra o menu na tela
def menu():
    while True:
        print("\n--- CLIENTE DE TRADUÇÃO ---")
        print("1. Traduzir um texto digitado")
        print("2. Traduzir um arquivo PDF")
        print("3. Ver histórico de traduções")
        print("0. Sair")  
        opcao = input("Escolha uma opção: ")

        # Opção 1: O usuário digita um texto e escolhe o idioma
        if opcao == "1":
            texto = input("Digite o texto (qualquer idioma): ")            
            print("Idiomas: en (Inglês), es (Espanhol), fr (Francês), de (Alemão), pt (Português)")
            idioma = input("Digite o código do idioma destino (ex: en): ")
            enviar_para_api(texto, idioma)
            
        # Opção 2: O usuário informa o caminho de um PDF
        elif opcao == "2":
            caminho = input("Digite o caminho do arquivo PDF (ex: documento.pdf): ")
            if not os.path.exists(caminho):
                print("Arquivo não encontrado!")
                continue
            
            print("Lendo PDF...")
            texto_pdf = ler_pdf(caminho)
            if texto_pdf:
                print(f"Texto extraído ({len(texto_pdf)} caracteres). Enviando para tradução...")               
                print("Idiomas: en (Inglês), es (Espanhol), fr (Francês), de (Alemão), pt (Português)")
                idioma = input("Digite o código do idioma destino (ex: en): ")
                
                # Pega só os primeiros 400 caracteres para não dar erro de limite na API
                texto_limitado = texto_pdf[:400] 
                enviar_para_api(texto_limitado, idioma)

        # Opção 3: Mostra o histórico de tudo que já foi traduzido
        elif opcao == "3":
            ver_historico()
            
        # Opção 0: Fecha o programa
        elif opcao == "0": 
            print("Saindo...")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

# Função que monta o pacote (JSON) e envia via POST para a nossa API
def enviar_para_api(texto, idioma):
    dados = {"texto": texto, "idioma_destino": idioma}
    try:
        resposta = requests.post(f"{URL_BASE}/traduzir", json=dados)
        if resposta.status_code == 200:
            resultado = resposta.json()
            if resultado["status"] == "sucesso":
                print(f"\n✅ Tradução: {resultado['dados']['traducao']}")
            else:
                print(f"\n❌ Erro na API: {resultado['mensagem']}")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Servidor fora do ar. Ligue o servidor primeiro.")

# Função que faz um GET na API para buscar o histórico salvo em memória
def ver_historico():
    try:
        resposta = requests.get(f"{URL_BASE}/historico")
        if resposta.status_code == 200:
            dados = resposta.json()
            print(f"\n--- HISTÓRICO ({dados['total']} registros) ---")
            for item in dados['historico']:
                print(f"[{item['id']}] {item['original'][:30]}... -> {item['traducao']} ({item['idioma_destino']})")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Servidor fora do ar.")

# Aqui é onde o programa começa de verdade
if __name__ == "__main__":
    menu()
