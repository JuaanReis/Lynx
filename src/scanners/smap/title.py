import requests
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

def get_title(url):
  """Pegar o título do site."""
  try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "Título não encontrado"
    return title
  except Exception as e:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar título: {e}"