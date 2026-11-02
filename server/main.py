from fastapi import FastAPI
from pydantic import BaseModel
from deep_translator import GoogleTranslator

app = FastAPI(title="API de Tradução - Mini Projeto 3")

historico_traducoes = []

class TextoRequest(BaseModel):
    texto: str
    idioma_destino: str = "en"

@app.post("/traduzir")
def traduzir_texto(dados: TextoRequest):
    try:
        traducao = GoogleTranslator(source='auto', target=dados.idioma_destino).translate(dados.texto)
        
        registro = {
            "id": len(historico_traducoes) + 1,
            "original": dados.texto,
            "traducao": traducao,
            "idioma_destino": dados.idioma_destino
        }
        historico_traducoes.append(registro)
        
        return {"status": "sucesso", "dados": registro}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/historico")
def obter_historico():
    return {"total": len(historico_traducoes), "historico": historico_traducoes}