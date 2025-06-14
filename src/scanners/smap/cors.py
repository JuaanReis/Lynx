import requests
from colorama import Fore, init
from src.utils.proxy import load_proxy
from src.utils.config import load_header

PROXY = load_proxy()
HEADERS = load_header()

init(autoreset=True)

def get_cors(url):
  """Verificar o CORS no site"""
  try:
    response = requests.get(url, timeout=10, headers=HEADERS, proxies=PROXY)
    cors = response.headers.get("Access-Control-Allow-Origin")
    if cors:
      if cors == "*":
        return f" CORS aberto para qualquer origem: {cors}"
      else:
        return f"CORS restrito para: {cors}"
    else:
      return "CORS Não encontrado"
  except Exception as e:
    return f" Erro ao verificar CORS: {e}"