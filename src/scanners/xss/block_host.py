from colorama import Fore, init
from urllib.parse import urlparse
from src.utils.config import load_host

init(autoreset=True)
host = load_host()

def block_host(args, host):
  parsed = urlparse(args.url)
  domain = parsed.netloc
  if domain.startswith("www."):
    domain = domain[4:]
  for k in host:
    if domain == k or domain.endswith("." + k):
      print(f"{Fore.RED}[!]{Fore.WHITE} Host {domain} esta bloqueado por motivos de segurança.")
      return True
  return False