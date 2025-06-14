import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from src.utils.proxy import load_proxy
from src.utils.config import load_header
from src.utils.prints import print_alert, print_data, print_item

PROXY = load_proxy()
HEADERS = load_header()

def get_internal_links(url):
    try:
        response = requests.get(url, timeout=10, headers=HEADERS, proxies=PROXY)
        soup = BeautifulSoup(response.text, "html.parser")
        domain = urlparse(url).netloc.lower()
        internos = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            parsed = urlparse(href)
            if parsed.scheme in ["http", "https"] and domain == parsed.netloc.lower():
                internos.add(href)
            elif href.startswith("/"):
                internos.add(f"{urlparse(url).scheme}://{domain}{href}")
        return list(internos)
    except Exception as e:
        return f"Erro ao coletar links internos {e}"

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
            return []
        return links
    except Exception as e:
        return [f"Erro ao coletar links externos: {e}"]

def get_all_links_recursive(url, max_depth=1, visitados=None):
    if visitados is None:
        visitados = set()
    if url in visitados or max_depth < 0:
        return []
    visitados.add(url)
    links_encontrados = []

    # Busca links internos
    internos = get_internal_links(url)
    if isinstance(internos, str):
        internos = []
    # Busca links externos
    externos = get_external_links(url)
    if isinstance(externos, str):
        externos = []

    todos_links = internos + externos

    for link in todos_links:
        if link not in visitados:
            links_encontrados.append(link)
            links_encontrados.extend(get_all_links_recursive(link, max_depth - 1, visitados))
    return list(set(links_encontrados))

def print_links_tree(url, max_depth=1, visitados=None, prefix=""):
  try:
    if visitados is None:
        visitados = set()
    if url in visitados or max_depth < 0:
        return
    visitados.add(url)
    # Busca links internos e externos
    from .links import get_internal_links, get_external_links
    internos = get_internal_links(url)
    externos = get_external_links(url)
    if isinstance(internos, str):
        internos = []
    if isinstance(externos, str):
        externos = []
    todos_links = internos + externos
    novos_links = [link for link in todos_links if link not in visitados]
    # Imprime o link raiz
    if prefix == "":
        print_data(f"Links a partir de: {url} com {max_depth} de profundidade")
        print_item(url)
    for i, link in enumerate(novos_links):
        is_last = i == len(novos_links) - 1
        branch = " └─ " if is_last else " ├─ "
        # Monta o prefixo para o próximo nível
        next_prefix = prefix + ("    " if is_last else " │   ")
        print(f"{prefix}{branch}{link}")
        print_links_tree(link, max_depth - 1, visitados, next_prefix)
  except Exception as e:
    print_alert("Erro ao imprimir links")