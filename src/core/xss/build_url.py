from urllib.parse import urlunparse

def build_url(parsed_url, new_query):
    """Monta a URL com os novos parâmetros de consulta."""
    scheme = parsed_url.scheme if not parsed_url.scheme.startswith("http") else "http"
    netloc = parsed_url.netloc if parsed_url.netloc else parsed_url.path.split("/")[0]
    path = parsed_url.path
    return urlunparse((scheme, netloc, path, parsed_url.params, new_query, parsed_url.fragment)).lstrip("/")