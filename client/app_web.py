import streamlit as st
import requests
from PyPDF2 import PdfReader

# URL da sua API (Servidor)
URL_API = "http://127.0.0.1:8000/traduzir"

st.set_page_config(page_title="Tradutor de PDF", page_icon="📄")

st.title("📄 Tradutor de Arquivos PDF")
st.write("Faça o upload de um PDF e traduza o texto usando nossa API.")

# Componente para upload de arquivo
arquivo_pdf = st.file_uploader("Escolha um arquivo PDF", type="pdf")

# Seletor de idioma
idioma_destino = st.selectbox(
    "Escolha o idioma de destino:",
    options=["en", "es", "fr", "de"],
    format_func=lambda x: {"en": "Inglês", "es": "Espanhol", "fr": "Francês", "de": "Alemão"}[x]
)

if st.button("Traduzir PDF"):
    if arquivo_pdf is not None:
        with st.spinner("Lendo o PDF..."):
            try:
                # Lendo o PDF diretamente da memória do navegador
                leitor = PdfReader(arquivo_pdf)
                texto_extraido = ""
                for pagina in leitor.pages:
                    texto_extraido += pagina.extract_text() + "\n"
                
                # Limitando o texto para não estourar o limite do Google Tradutor
                texto_limitado = texto_extraido[:2000].strip()
                
                if not texto_limitado:
                    st.error("Não foi possível extrair texto deste PDF (pode ser uma imagem escaneada).")
                else:
                    with st.spinner("Enviando para a API e traduzindo..."):
                        # Consumindo a API (POST)
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
