import subprocess
import time
import sys

print("Iniciando o Servidor (API)...")
# Inicia a API em segundo plano
servidor = subprocess.Popen([sys.executable, "-m", "uvicorn", "server.main:app", "--reload"])

# Espera 2 segundos para o servidor ligar antes de abrir o navegador
time.sleep(2)

print("Iniciando o Cliente Web (Streamlit)...")
# Inicia o Streamlit (que abre o navegador)
cliente = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "client/app_web.py"])

# Mantém os dois rodando até que o usuário feche o Streamlit
cliente.wait()
servidor.terminate()
