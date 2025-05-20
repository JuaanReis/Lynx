from urllib.parse import urlparse
from colorama import Fore, init

init(autoreset=True)

def get_domain(url):
  """Verificar o domínio da URL."""
  parsed_url = urlparse(url)
  domain = parsed_url.netloc
  return f"{Fore.CYAN}{domain}"