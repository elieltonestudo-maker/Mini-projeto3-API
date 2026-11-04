import streamlit as st
import requests
from PyPDF2 import PdfReader

# Endereço da nossa API (o servidor)
URL_API = "http://127.0.0.1:8000/traduzir"

# Configuração básica da página do navegador
st.set_page_config(page_title="Tradutor Inteligente", page_icon="🌍")

# Título e texto que aparecem na tela
st.title("🌍 Tradutor Inteligente")
st.write("Traduza textos ou arquivos PDF (com detecção automática de idioma).")

# Menu para escolher o idioma de destino
idioma_destino = st.selectbox(
    "Escolha o idioma de destino:",
    options=["en", "es", "fr", "de", "pt"], 
    format_func=lambda x: {
        "en": "Inglês", 
        "es": "Espanhol", 
        "fr": "Francês", 
        "de": "Alemão",
        "pt": "Português" # <-- Adicionado aqui
    }[x]
)

# Cria duas abas na tela: uma para Texto e outra para PDF
aba_texto, aba_pdf = st.tabs(["📝 Digitar Texto", "📄 Enviar PDF"])

# --- ABA 1: TEXTO DIGITADO ---
with aba_texto:
    texto_digitado = st.text_area("Digite ou cole o texto que deseja traduzir:")
    
    if st.button("Traduzir Texto"):
        if texto_digitado.strip():
            with st.spinner("Traduzindo texto..."):
                dados = {"texto": texto_digitado, "idioma_destino": idioma_destino}
                try:
                    resposta = requests.post(URL_API, json=dados)
                    if resposta.status_code == 200:
                        resultado = resposta.json()
                        if resultado["status"] == "sucesso":
                            st.success("Tradução concluída!")
                            st.subheader("Tradução:")
                            st.info(resultado['dados']['traducao'])
                        else:
                            st.error(f"Erro na API: {resultado['mensagem']}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro: O servidor não está rodando. Ligue o servidor primeiro.")
        else:
            st.warning("Por favor, digite um texto antes de traduzir.")

# --- ABA 2: UPLOAD DE PDF ---
with aba_pdf:
    arquivo_pdf = st.file_uploader("Escolha um arquivo PDF", type="pdf")
    
    if st.button("Traduzir PDF"):
        if arquivo_pdf is not None:
            with st.spinner("Lendo o PDF..."):
                try:
                    # Abre o PDF direto da memória do navegador
                    leitor = PdfReader(arquivo_pdf)
                    texto_extraido = ""
                    # Junta o texto de todas as páginas
                    for pagina in leitor.pages:
                        texto_extraido += pagina.extract_text() + "\n"
                    
                    # Pega só os primeiros 400 caracteres para não estourar o limite do MyMemory
                    texto_limitado = texto_extraido[:400].strip()
                    
                    if not texto_limitado:
                        st.error("Não foi possível extrair texto deste PDF (pode ser uma imagem escaneada).")
                    else:
                        with st.spinner("Enviando para a API e traduzindo..."):
                            dados = {"texto": texto_limitado, "idioma_destino": idioma_destino}
                            resposta = requests.post(URL_API, json=dados)
                            
                            if resposta.status_code == 200:
                                resultado = resposta.json()
                                if resultado["status"] == "sucesso":
                                    st.success("Tradução concluída!")
                                    st.subheader("Texto Original (Trecho):")
                                    st.info(texto_limitado)
                                    st.subheader("Tradução:")
                                    st.success(resultado['dados']['traducao'])
                                else:
                                    st.error(f"Erro na API: {resultado['mensagem']}")
                except Exception as e:
                    st.error(f"Erro ao processar o arquivo: {e}")
        else:
            st.warning("Por favor, faça o upload de um arquivo PDF primeiro.")
