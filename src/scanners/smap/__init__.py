import logging
from colorama import Fore, init
from .tecnologies import get_tecnologies
from .headers import get_headers
from .port import get_port
from .protocol import get_protocol
from .forms import get_forms
from .domain import get_domain
from .ssl import get_ssl
from .cors import get_cors
from .cookies import get_cookies
from .links import get_external_links, get_internal_links
from .title import get_title
from .params import get_params
from src.utils.file_logs import setup_logs
import argparse

init(autoreset=True)

setup_logs()

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

#flags
def run(user_args=None):
  """Executar o scanner geral."""
  parser = argparse.ArgumentParser(description="scanner geral")
  parser.add_argument("-u", "--url", required=True, help="URL do login")
  args = parser.parse_args(user_args)
  url = args.url
  main(url)

#Função principal
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
  try:
     run()
  except Exception as e:
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao executar o scanner: {e}")
    logging.error(f"Erro ao executar o scanner: {e}")