import requests
import os
from PyPDF2 import PdfReader

URL_BASE = "http://127.0.0.1:8000"

def ler_pdf(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto_completo = ""
        for pagina in leitor.pages:
            texto_completo += pagina.extract_text() + "\n"
        return texto_completo.strip()
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None

def menu():
    while True:
        print("\n--- CLIENTE DE TRADUÇÃO ---")
        print("1. Traduzir um texto digitado")
        print("2. Traduzir um arquivo PDF")
        print("3. Ver histórico de traduções")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            texto = input("Digite o texto (Português): ")
            print("Idiomas: en (Inglês), es (Espanhol), fr (Francês)")
            idioma = input("Digite o código do idioma destino (ex: en): ")
            enviar_para_api(texto, idioma)
            
        elif opcao == "2":
            caminho = input("Digite o caminho do arquivo PDF (ex: documento.pdf): ")
            if not os.path.exists(caminho):
                print("Arquivo não encontrado!")
                continue
            
            print("Lendo PDF...")
            texto_pdf = ler_pdf(caminho)
            if texto_pdf:
                print(f"Texto extraído ({len(texto_pdf)} caracteres). Enviando para tradução...")
                print("Idiomas: en (Inglês), es (Espanhol), fr (Francês)")
                idioma = input("Digite o código do idioma destino (ex: en): ")
                
                # Dica: APIs têm limite de tamanho. Se o PDF for enorme, pode dar erro.
                # Para o projeto, vamos enviar apenas os primeiros 2000 caracteres para garantir.
                texto_limitado = texto_pdf[:2000] 
                enviar_para_api(texto_limitado, idioma)

        elif opcao == "3":
            ver_historico()
        elif opcao == "4":
            break

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
        print("\n❌ ERRO: Servidor fora do ar.")

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

if __name__ == "__main__":
    menu()
