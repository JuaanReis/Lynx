import requests
from colorama import Fore, init
from urllib.parse import urlparse
from bs4 import BeautifulSoup

init(autoreset=True)

#Pegar links internos de uma url
def get_internal_links(url):
  try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    domain = urlparse(url).netloc.lower()
    internos = []
    for a in soup.find_all("a", href=True):
      href = a["href"]
      parsed = urlparse(href)
      if parsed.scheme in ["http", "https"] and domain == parsed.netloc.lower():
        internos.append(href)
      elif href.startswith("/"):
        internos.append(f"{urlparse(url).scheme}://{domain}{href}")
    return internos
  except Exception:
    return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar links internos."]

#Pegar links externos de uma url
def get_external_links(url):
  """Pegar links externos do site"""
  try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    domain = urlparse(url).netloc.lower()
    for a in soup.find_all("a", href=True):
      href = a["href"]
      parsed = urlparse(href)
      if parsed.scheme in ["http", "https"]:
        link_domain = parsed.netloc.lower()
        if link_domain and link_domain != domain:
          links.append(href)
    if not links:
      return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum link externo encontrado."]
    return links
  except Exception as e:
    return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar links externos: {e}"]