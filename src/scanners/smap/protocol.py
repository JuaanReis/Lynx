from colorama import Fore, init
from urllib.parse import urlparse

init(autoreset=True)

def get_protocol(url):
  """Verificar o protocolo utilizado na URL (HTTP ou HTTPS)."""
  parsed_url = urlparse(url)
  if parsed_url.scheme == "https":
    return f"{Fore.GREEN}->" + f"{Fore.WHITE} Protocolo: HTTPS" + f"{Fore.GREEN} Seguro" + f"{Fore.WHITE}(SSL)"
  elif parsed_url.scheme == "http":
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Protocolo: HTTP" + f"{Fore.RED} Inseguro"
  else:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Protocolo desconhecido: {parsed_url.scheme}"