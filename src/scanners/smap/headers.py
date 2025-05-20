import requests
from colorama import Fore, init

init(autoreset=True)

def get_headers(url):
  """Coleta os cabeçalhos do site e verifica se algum cabeçalho padrão está faltando."""

  try:
    response = requests.get(url, timeout=10)
    headers = response.headers
    return dict(headers)
  except requests.RequestException as e:
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar cabeçalhos: {e}")
    return {}