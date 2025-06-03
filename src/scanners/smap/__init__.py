import logging
from colorama import Fore, init
import argparse
import json
from .tecnologies import get_tecnologies
from .headers import get_headers
from .port import scan_ports
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

init(autoreset=True)
setup_logs()

with open("./src/scanners/smap/ports.json", "r") as f:
    PORTS = json.load(f)

# Cabeçalhos recomendados
HEADERS_RECOMENDADOS = [
    "Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options",
    "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy",
    "X-XSS-Protection",
    "Access-Control-Allow-Origin"
]

def run(user_args=None):
    parser = argparse.ArgumentParser(description="Scanner geral")
    parser.add_argument("-u", "--url", required=True, help="URL do alvo")
    args = parser.parse_args(user_args)
    main(args.url)

def print_header(msg, color=Fore.GREEN):
    print(f"{color}[+]{Fore.WHITE} {msg}")

def print_sub(msg, color=Fore.YELLOW):
    print(f"  {color}->{Fore.WHITE} {msg}")

def print_error(msg):
    print(f"{Fore.RED}[-]{Fore.WHITE} {msg}")

def print_warning(msg):
    print(f"{Fore.YELLOW}[!]{Fore.WHITE} {msg}")

def main(url):
    try:
        print_header("Logs sendo emitidos...")

        # Coleta de dados
        headers = get_headers(url)
        protocols = get_protocol(url)
        forms = get_forms(url)
        title = get_title(url)
        domain = get_domain(url)
        ssl_info = get_ssl(url)
        cors_status = get_cors(url)
        tecnologias = get_tecnologies(url)
        cookies = get_cookies(url)
        external_links = get_external_links(url)
        internal_links = get_internal_links(url)
        host = domain
        portC = [p["port"] for p in PORTS]
        open_ports = scan_ports(host, portC)

        # Logs
        logging.info(f"URL: {url}")
        logging.info(f"Protocolo: {protocols}")
        logging.info(f"Porta: {open_ports}")
        logging.info(f"Domínio: {domain}")
        logging.info(f"SSL: {ssl_info}")
        logging.info(f"CORS: {cors_status}")
        logging.info(f"Cookies: {cookies}")
        logging.info(f"Forms: {forms}")
        logging.info(f"Links externos: {external_links}")
        logging.info(f"Links internos: {internal_links}")
        logging.info(f"Parâmetros: {get_params([url])}")
        logging.info(f"Tecnologias: {tecnologias}")

        print_warning("Resumo da análise:")
        print_header(f"URL: {url}")
        print_header(f"Protocolo: {protocols}")
        print_header(f"CORS: {cors_status}")
        print_header(f"SSL: {ssl_info.get('status', 'desconhecido')}")

        if ssl_info.get('status') == 'erro':
            print_error(f"Erro no SSL: {ssl_info.get('message')}")
        if not ssl_info.get('status'):
            print_error("SSL não está configurado corretamente.")
        else:
            for key in ['issuer', 'serialNumber', 'version', 'notBefore', 'notAfter']:
                print_sub(f"{key}: {ssl_info.get(key)}")

        print_header(f"Domínio: {domain}")
        print_header(f"Título: {title}")
        print_header(f"Portas: {len(open_ports)}")
        if open_ports:
            port_service = {p["port"]: p["service"] for p in PORTS}
            for porta in open_ports:
                servico = port_service.get(porta, "desconhecido")
                print_sub(f"Portas abertas: {porta} ({servico})")
        else:
            print_sub(f"Nenhuma porta aberta")

        # Cabeçalhos
        presentes = [h for h in HEADERS_RECOMENDADOS if h in headers]
        ausentes = [h for h in HEADERS_RECOMENDADOS if h not in headers]

        for h in presentes:
            print_header(f"Cabeçalho presente: {h}")
        for h in ausentes:
            print_sub(f"Cabeçalho ausente: {h}", color=Fore.RED)

        if ausentes:
            print_warning(f"Adicione os cabeçalhos: {', '.join(ausentes)}")
        else:
            print_header("Todos os cabeçalhos estão presentes!")

        # Cookies
        print_header("Cookies encontrados:")
        if cookies:
            for c in cookies:
                print_sub(c)
        else:
            print_sub("Nenhum cookie encontrado.", color=Fore.RED)

        # Forms
        print_header(f"Formulários encontrados: {len(forms)}")
        for i, form in enumerate(forms, 1):
            print_sub(f"Formulário #{i}")
            print_sub(f"Método: {form['method']}")
            print_sub(f"Action: {form['action']}")
            for campo in form['inputs']:
                tipo = "[HIDDEN]" if campo['type'].lower() == 'hidden' else "Campo"
                print_sub(f"{tipo} - Nome: {campo['name']} | Valor: {campo['value']}",
                          color=Fore.YELLOW if tipo == "[HIDDEN]" else Fore.GREEN)

        # Links
        print_header("Links externos:")
        for link in external_links:
            print_sub(link)

        print_header("Links internos:")
        for link in internal_links:
            print_sub(link)

        # Parâmetros
        print_header("Parâmetros URL principal:")
        for p in get_params([url]):
            print_sub(p)

        print_header("Parâmetros links internos:")
        for p in get_params(internal_links):
            print_sub(p)

        print_header("Parâmetros links externos:")
        for p in get_params(external_links):
            print_sub(p)

        # Tecnologias
        print_header("Tecnologias detectadas:")
        for k, v in tecnologias.items():
            if isinstance(v, list):
                print_sub(f"{k}:")
                for item in v:
                    print_sub(f"{item}")
            else:
                print_sub(f"{k}: {v}")

        print_header("Verificação concluída com sucesso!")

    except Exception as e:
        print_error(f"Erro na verificação da URL: {e}")
        logging.error(f"Erro na verificação: {e}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print_error(f"Erro na execução do scanner: {e}")
        logging.error(f"Erro na execução do scanner: {e}")