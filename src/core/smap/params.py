from colorama import Fore, init
from urllib.parse import urlparse, parse_qs

init(autoreset=True)

def get_params(url):
  """Pega os parametros da URL e os externos"""
  perigoso = {
    # Geral (XSS, SQLi, IDOR, etc.)
    "id", "uid", "user", "userid", "username", "account", "profile", "client",
    "member", "student", "contact", "customer", "empid", "admin",
    # Busca / Entrada de texto (XSS, SQLi)
    "q", "query", "search", "s", "keyword", "lang", "term", "text", "message",
    "input", "title", "desc", "filter", "where", "sort", "order", "select",
    # Autenticação / CSRF
    "pass", "password", "email", "token", "csrf", "xsrf", "auth",
    "authorization", "access_token",
    # Upload
    "filename", "file", "upload", "image", "photo", "avatar", "doc", "pdf",
    # Inclusão de arquivos (LFI, RFI)
    "file", "filepath", "path", "page", "template", "include", "folder",
    "dir", "route", "view", "download",
    # Redirecionamento aberto
    "url", "next", "return", "redir", "redirect", "dest", "destination",
    "continue", "callback", "back", "link", "site", "domain",
    # RCE
    "cmd", "exec", "execute", "run", "shell", "code", "call",
    # SSRF
    "remote", "proxy", "img", "image", "uri",
    # Outros suspeitos
    "debug", "test", "json", "config", "env", "dev", "mode"
  }
  resultado = []
  for url in url:
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if params:
      for nome in params:
        perigo = f"{Fore.RED}[PERIGOSO]" if nome.lower() in perigoso else ""
        resultado.append(f"{url}" + f"{Fore.GREEN} ->   " + f"{nome}: {params[nome]} {perigo}")
  return resultado if resultado else ["Nenhum parametro encontrado."]