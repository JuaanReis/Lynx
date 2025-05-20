from colorama import Fore, init
from urllib.parse import urlparse, parse_qs

init(autoreset=True)

def get_port(url):
  """Verificar a porta utilizada na URL."""
  try:
    port = urlparse(url).port
    if port is None:
      port = 80 if urlparse(url).scheme == "http" else 443
    return port
  except Exception as e:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao verificar a porta: {e}"