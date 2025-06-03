from urllib.parse import urlparse

def get_domain(url):
  """Verificar o domínio da URL."""
  try:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return f"{domain}"
  except Exception as e:
    print(f"Erro ao extrair o domínio da URL: {e}")