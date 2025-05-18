import requests
import argparse
from urllib.parse import urlparse, parse_qs
from colorama import Fore, init
from bs4 import BeautifulSoup
import ssl
from datetime import datetime
import socket
import logging
from src.utils.file_logs import setup_logs

setup_logs()

init(autoreset=True)

def run(user_args=None):
  """Executar o scanner geral."""
  parser = argparse.ArgumentParser(description="scanner geral")
  parser.add_argument("-u", "--url", required=True, help="URL do login")
  args = parser.parse_args(user_args)
  url = args.url
  main(url)

#Pegar cookies do site
def get_cookies(url):
  try:
    response = requests.get(url, timeout=10)
    cookies = response.cookies
    if not cookies:
      return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum cookie encontrado."]
    detalhes = []
    for cookie in cookies:
      info = f"{cookie.name}={cookie.value}"
      info += f" | Domain: {cookie.domain}"
      info += f" | Path: {cookie.path}"
      info += f" | Secure: {cookie.secure}"
      info += f" | HttpOnly: {getattr(cookie, 'httponly', False)}"
      info += f" | SameSite: {getattr(cookie, 'samesite', 'Não informado')}"
      info += f" | Expires: {cookie.expires if cookie.expires else 'Não informado'}"
      detalhes.append(info)
    return detalhes
  except Exception as e:
    return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar cookies: {e}"]

#Pegar links externas
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

#Pegar links internos
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

#Pegar os parametros da URL e externo
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

#Detectar a tecnologia do site
def get_tecnologies(url):
  """Detecta a tecnologia por tras do site"""
  try:
    response = requests.get(url, timeout=10)
    headers = response.headers
    tecnologias = {}

    #Servidor web
    if "Server" in headers:
      tecnologias["Servidor"] = headers["Server"]

    #Backend comum
    backends = []
    if "X-Powered-By" in headers:
      backends.append(headers["X-Powered-By"])
    if "X-AspNet-Version" in headers:
      backends.append("ASP.NET " + headers["X-AspNet-Version"])
    if backends:
      tecnologias["Backend"] = backends

    #CDN comum
    cdn_headers = [
      ("Cloudflare", "CF-RAY"),
      ("Akamai", "X-Akamai-Transformed"),
      ("Sucuri", "X-Sucuri-ID"),
      ("Fastly", "Fastly-SSL"),
      ("Amazon CloudFront", "X-Amz-Cf-Id"),
      ("StackPath", "X-CDN"),
      ("Incapsula", "X-CDN"),
      ("Google", "X-Goog-Hash"),
    ]
    cdns = []
    for nome, cab in cdn_headers:
      if cab in headers:
        cdns.append(nome)
    if cdns:
      tecnologias["CDN"] = cdns

    #APIs detectadas
    apis = []
    for k, v in headers.items():
      if "api" in k.lower() or "api" in v.lower():
        apis.append(f"{k}: {v}")
    if apis:
      tecnologias["APIs"] = apis

    return tecnologias if tecnologias else {"Info": "Nenhuma tecnologia detectada"}
  except Exception as e:
    return {"Erro": str(e)}

#Verificar o CORS
def get_cors(url):
  """Verificar o CORS no site"""
  try:
    response = requests.get(url, timeout=10)
    cors = response.headers.get("Access-Control-Allow-Origin")
    if cors:
      if cors == "*":
        return f"{Fore.GREEN}[!]" + f"{Fore.WHITE} CORS aberto para qualquer origem: {cors}"
      else:
        return f"{Fore.RED}[-]" + f"{Fore.WHITE} CORS restrito para: {cors}"
    else:
      return f"{Fore.RED}[-]" + f"{Fore.WHITE} CORS:" + f"{Fore.RED} Não encontrado"
  except Exception as e:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao verificar CORS: {e}"

#Pegar o titulo do site
def get_title(url):
  """Pegar o título do site."""
  try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "Título não encontrado"
    return title
  except Exception as e:
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar título: {e}")
    return

# Verificar qual protocolo é utilizado
def get_protocol(url):
  """Verificar o protocolo utilizado na URL (HTTP ou HTTPS)."""
  parsed_url = urlparse(url)
  if parsed_url.scheme == "https":
    return f"{Fore.GREEN}->" + f"{Fore.WHITE} Protocolo: HTTPS" + f"{Fore.GREEN} Seguro" + f"{Fore.WHITE}(SSL)"
  elif parsed_url.scheme == "http":
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Protocolo: HTTP" + f"{Fore.RED} Inseguro"
  else:
    return f"{Fore.RED}[-]" + f"{Fore.WHITE} Protocolo desconhecido: {parsed_url.scheme}"

# Verificar a porta utilizada
def get_port(url):
  """Verificar a porta utilizada na URL."""
  try:
    port = urlparse(url).port
    if port is None:
      port = 80 if urlparse(url).scheme == "http" else 443
    return port
  except Exception as e:
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao verificar a porta: {e}")
    return

#Verificar o certificado SSL
def get_ssl(url):
  """Verificar o certificado SSL do site"""
  hostname = urlparse(url).hostname
  context = ssl.create_default_context()
  try:
    with socket.create_connection((hostname, 443), timeout=10) as sock:
      with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        cert = ssock.getpeercert()
        espira = datetime.strptime(cert.get('notAfter'), '%b %d %H:%M:%S %Y %Z')
        status = "valido" if espira > datetime.now() else "expirado"
        return {
          "status": status,
          "validade": espira.strftime('%Y-%m-%d %H:%M:%S'),
          "issuer": dict(x[0] for x in cert['issuer']),
          "subject": dict(x[0] for x in cert['subject']),
          "serialNumber": cert['serialNumber'],
          "version": cert['version'],
          "notBefore": cert['notBefore'],
          "notAfter": cert['notAfter']
        }
  except Exception as e:
    return {"status": "erro", "message": str(e)}

# Verificar o domínio
def get_domain(url):
  """Verificar o domínio da URL."""
  parsed_url = urlparse(url)
  domain = parsed_url.netloc
  return domain

# Pegar os cabeçalhos do site e ver qual que falta
def get_headers(url):
  """Coleta os cabeçalhos do site e verifica se algum cabeçalho padrão está faltando."""

  try:
    response = requests.get(url, timeout=10)
    headers = response.headers
    return dict(headers)
  except requests.RequestException as e:
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar cabeçalhos: {e}")
    return {}

# Verificar formularios
def get_forms(url):
    """Verificar quais formulários estão disponíveis na URL e retornar método, action e campos."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        all_forms = []
        for form in forms:
            form_info = {
                "action": form.get("action", ""),
                "method": form.get("method", "GET").upper(),
                "inputs": []
            }
            inputs = form.find_all("input")
            for input_tag in inputs:
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name", "")
                input_value = input_tag.get("value", "")
                form_info["inputs"].append({
                    "type": input_type,
                    "name": input_name,
                    "value": input_value
                })
            all_forms.append(form_info)
        return all_forms
    except Exception as e:
        return []

def main(url):
  try:
    headers = get_headers(url)
    protocols = get_protocol(url)
    forms = get_forms(url)
    port = get_port(url)
    domain = get_domain(url)
    ssl_info = get_ssl(url)
    cors_status = get_cors(url)
    tecnologias = get_tecnologies(url)
    cookies = get_cookies(url)
    external_links = get_external_links(url)
    internal_links = get_internal_links(url)

    #Logs
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Logs sendo emitiados...")
    logging.info(f"URL: {url}")
    logging.info(f"Protocolo: {protocols}")
    logging.info(f"Porta: {port}")
    logging.info(f"Domínio: {domain}")
    logging.info(f"SSL: {ssl_info['status']}")
    logging.info(f"CORS: {cors_status}")
    logging.info(f"Cookies: {cookies}")
    logging.info(f"Formulários: {len(forms)} encontrados.")
    for i, form in enumerate(forms):
        logging.info(f"Formulário #{i+1}:")
        logging.info(f"  Método: {form['method']}")
        logging.info(f"  Action: {form['action']}")
        for campo in form["inputs"]:
            if campo["type"].lower() == "hidden":
                logging.info(f"    [HIDDEN] Nome: {campo['name']} | Valor: {campo['value']}")
            else:
                logging.info(f"    Tipo: {campo['type']} | Nome: {campo['name']} | Valor: {campo['value']}")
    logging.info(f"Links externos encontrados: {external_links}")
    logging.info(f"Links internos encontrados: {internal_links}")
    logging.info(f"Parâmetros encontrados na URL principal: {get_params([url])}")
    logging.info(f"Parâmetros encontrados nos links internos: {get_params(internal_links)}")
    logging.info(f"Parâmetros encontrados nos links externos: {get_params(external_links)}")
    logging.info(f"Tecnologias detectadas: {tecnologias}")
    logging.info(f"Verificação concluída com sucesso!")

    # Lista de cabeçalhos recomendados
    headers_recomendados = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
        "X-XSS-Protection",
        "Access-Control-Allow-Origin"
    ]
    presentes = [header for header in headers_recomendados if header in headers]
    ausentes = [header for header in headers_recomendados if header not in headers]

    print(f"{Fore.RED}[!]" + f"{Fore.WHITE} Resumo da analise:" )
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} URL: {url}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Protocolo: {protocols}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} CORS: {cors_status}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} SSL: {ssl_info['status']}")
    if ssl_info['status'] == "erro":
      print(f"  {Fore.RED}[-]" + f"{Fore.WHITE} Erro ao verificar o SSL: {ssl_info['message']}")
    else:
      print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} Emissor: {str(ssl_info['issuer'])}")
      print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} Serial Number: {ssl_info['serialNumber']}")
      print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} Versão: {ssl_info['version']}")
      print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} Validade: {ssl_info['notBefore']} - {ssl_info['notAfter']}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Porta: {port}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Domínio: {domain}")
    for h in presentes:
      print(f"{Fore.GREEN}[+]{Fore.WHITE} Cabeçalho presente: {h}")
    for h in ausentes:
      print(f"  {Fore.RED} ->{Fore.WHITE} Cabeçalho ausente: {h}")
    if ausentes:
      print(f"{Fore.YELLOW}[!]{Fore.WHITE} Recomendado adicionar o(s) cabeçalho(s): {', '.join(ausentes)}")
    else:
      print(f"{Fore.GREEN}[+]{Fore.WHITE} Todos os cabeçalhos recomendados estão presentes!")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Título: {get_title(url)}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Cookies encontrados:")
    if cookies:
      for cookie in cookies:
        print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} {cookie}")
    else:
      print(f"  {Fore.RED}->" + f"{Fore.WHITE} Nenhum cookie encontrado.")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Formulários: {len(forms)} encontrados.")
    for i, form in enumerate(forms):
        print(f"  {Fore.GREEN}>{Fore.WHITE} Formulário #{i+1}:")
        print(f"    Método: {form['method']}")
        print(f"    Action: {form['action']}")
        for campo in form["inputs"]:
            if campo["type"].lower() == "hidden":
                print(f"      {Fore.YELLOW}[HIDDEN]{Fore.WHITE} Nome: {campo['name']} | Valor: {campo['value']}")
            else:
                print(f"      Tipo: {campo['type']} | Nome: {campo['name']} | Valor: {campo['value']}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Links externos encontrados:")
    for link in external_links:
      print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} {link}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Parametros encontrados na URL principal:")
    for param in get_params([url]):
      print(f"  {Fore.GREEN} ->" + f"{Fore.WHITE} {param}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Parametros encontrados nos links internos:")
    for param in get_params(internal_links):
      print(f"  {Fore.GREEN} ->" + f"{Fore.WHITE} {param}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Parametros encontrados nos links externos:")
    for param in get_params(external_links):
      print(f"  {Fore.GREEN} ->" + f"{Fore.WHITE} {param}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Tecnologias detectadas:")
    for k, v in tecnologias.items():
      if isinstance(v, list):
        print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} {k}:")
        for item in v:
          print(f"    {Fore.GREEN}>" + f"{Fore.WHITE} {item}")
      else:
        print(f"  {Fore.GREEN}->" + f"{Fore.WHITE} {k}: {v}")
    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Verificação concluída com sucesso!")
  except Exception as e:
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao verificar a URL: {e}")

if __name__ == "__main__":
  run()