from fastapi import FastAPI
from pydantic import BaseModel
from deep_translator import MyMemoryTranslator
from langdetect import detect

# Cria a aplicação FastAPI
app = FastAPI(title="API de Tradução - Mini Projeto 3")

# Lista que guarda o histórico de traduções na memória
historico_traducoes = []

# Define o formato dos dados que o cliente vai enviar (texto e idioma destino)
class TextoRequest(BaseModel):
    texto: str
    idioma_destino: str = "en"

# Rota POST para receber o texto e devolver a tradução
@app.post("/traduzir")
def traduzir_texto(dados: TextoRequest):
    try:
        # 1. O sistema descobre sozinho qual é o idioma do texto que chegou
        idioma_origem = detect(dados.texto)
        
        # 2. Prepara os códigos de idioma no formato que a API do MyMemory exige
        mapa_origem = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR", "de": "de-DE"}
        mapa_destino = {"en": "en-US", "es": "es-ES", "fr": "fr-FR", "de": "de-DE", "pt": "pt-BR"}
        
        source = mapa_origem.get(idioma_origem, "pt-BR")
        target = mapa_destino.get(dados.idioma_destino, "en-US")

        # Se o idioma de origem for igual ao de destino, não precisa traduzir
        if source == target:
            traducao = dados.texto
        else:
            # Faz a tradução usando a biblioteca
            traducao = MyMemoryTranslator(source=source, target=target).translate(dados.texto)
        
        # Monta o registro com os dados da tradução
        registro = {
            "id": len(historico_traducoes) + 1,
            "original": dados.texto,
            "traducao": traducao,
            "idioma_origem": source,
            "idioma_destino": target
        }
        # Salva no histórico
        historico_traducoes.append(registro)
        
        return {"status": "sucesso", "dados": registro}
    except Exception as e:
        # Se der algum erro, avisa o cliente
        return {"status": "erro", "mensagem": str(e)}

# Rota GET para o cliente consultar o histórico de traduções
@app.get("/historico")
def obter_historico():
    return {"total": len(historico_traducoes), "historico": historico_traducoes}