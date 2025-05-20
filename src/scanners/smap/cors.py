import requests
from colorama import Fore, init

init(autoreset=True)

def get_cors(url):
  """Verificar o CORS no site"""
  try:
    response = requests.get(url, timeout=10)
    cors = response.headers.get("Access-Control-Allow-Origin")
    if cors:
      if cors == "*":
        return f"{Fore.GREEN}[!]" + f"{Fore.WHITE} CORS aberto para qualquer origem: {cors}"
      else:
        return f"{Fore.RED}[-]" + f"{Fore.WHITE} CORS restrito para: {cors}"
    else:
      return f"{Fore.RED}[-]" + f"{Fore.WHITE} CORS:" + f"{Fore.RED} Não encontrado"
  except Exception as e:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao verificar CORS: {e}"