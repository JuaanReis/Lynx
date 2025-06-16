import requests
from colorama import Fore, init
from bs4 import BeautifulSoup
from src.utils.proxy import load_proxy
from src.utils.config import load_header

PROXY = load_proxy()
HEADERS = load_header()

init(autoreset=True)

def get_title(url):
  """Pegar o título do site."""
  try:
    response = requests.get(url, timeout=10, headers=HEADERS, proxies=PROXY)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "Título não encontrado"
    return title
  except Exception as e:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar título: {e}"