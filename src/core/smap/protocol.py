from colorama import Fore, init
from urllib.parse import urlparse

init(autoreset=True)

def get_protocol(url):
  """Verificar o protocolo utilizado na URL (HTTP ou HTTPS)."""
  try:
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme.upper()
    return protocol
  except Exception as e:
    return f"{Fore.RED}Erro ao obter protocolo: {e}"