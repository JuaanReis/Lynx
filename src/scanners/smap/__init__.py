import logging
import argparse
import json
from urllib.parse import urlparse
from .tecnologies import get_tecnologies
from .headers import get_headers
from .port import scan_ports
from .protocol import get_protocol
from .forms import get_forms
from .domain import get_domain
from .ssl import get_ssl
from .cors import get_cors
from .cookies import get_cookies
from .links import get_external_links, get_internal_links, get_all_links_recursive, print_links_tree
from .title import get_title
from .params import get_params
from .ip import get_ipv4, get_ipv6
from src.utils.file_logs import setup_logs
from src.utils.config import load_host
from src.utils.prints import print_data, print_alert, print_hack, print_item, print_item_c,print_item_c_esc, print_end_item, print_sub_item,print_sub_item_esc, print_item_esc, print_end_item_esc

setup_logs()

host = load_host()

with open("./src/scanners/smap/ports.json", "r") as f:
    PORTS = json.load(f)

with open("./src/scanners/smap/headers_r.json", "r") as f:
    HEADERS_RECOMENDADOS = json.load(f)

# Cabeçalhos recomendados
HEADERS_RECOMENDADOS = HEADERS_RECOMENDADOS.get("headers_personalizados", [])

def main(url, args):
    try:
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
        all_links = get_all_links_recursive(url)
        host = domain
        portC = [p["port"] for p in PORTS]
        open_ports = scan_ports(host, portC)
        ipv4 = get_ipv4(host)
        ipv6 = get_ipv6(host)

            # Logs
        if args.log:
            logging.info(f"URL: {url}")
            logging.info(f"IPv4: {ipv4}")
            logging.info(f"IPv6: {ipv6}")
            logging.info(f"Protocolo: {protocols}")
            logging.info(f"Porta: {open_ports}")
            logging.info(f"Domínio: {domain}")
            logging.info(f"SSL: {ssl_info}")
            logging.info(f"CORS: {cors_status}")
            logging.info(f"Cookies: {len(cookies)}")
            logging.info(f"Forms: {forms}")
            logging.info(f"Links externos: {external_links}")
            logging.info(f"Links internos: {internal_links}")
            logging.info(f"Parâmetros: {get_params([url])}")
            logging.info(f"Tecnologias: {tecnologias}")


        print_hack(f"Target ->  {url}")
        print_hack(f"IPv4 ->  {ipv4}")
        print_hack(f"IPv6 ->  {ipv6}")
        print_hack(f"Domain ->  {domain}")
        print_hack(f"Title ->   {title}")
        print_hack(f"Protocol ->    {protocols}")
        print_hack(f"SSL ->    {ssl_info.get('status', 'desconhecido')}")
        if ssl_info.get('status') == 'erro':
            print_alert(f"Erro no SSL: {ssl_info.get('message')}")
        if not ssl_info.get('status'):
            print_alert("SSL não está configurado corretamente.")
        else:
            for i, key in enumerate(['issuer', 'serialNumber', 'version', 'notBefore', 'notAfter']):
                if i == len(['issuer', 'serialNumber', 'version', 'notBefore', 'notAfter']) - 1:
                    print_end_item(f"{key}: {ssl_info.get(key)}\n")
                else:
                    print_item(f"{key}: {ssl_info.get(key)}")


        print_data(f"Ports open: {len(open_ports)}")
        if open_ports:
            port_service = {p["port"]: p["service"] for p in PORTS}
            for i, porta in enumerate(open_ports):
                servico = port_service.get(porta, "desconhecido")
                if i == len(open_ports) - 1:
                    print_end_item(f"{porta} ({servico})\n")
                else:
                    print_item(f"{porta} ({servico})")
        else:
            print_item(f"Nenhuma porta aberta\n")

        print_data(f"Headers security")
        # Cabeçalhos
        presentes = [h for h in HEADERS_RECOMENDADOS if h in headers]
        ausentes = [h for h in HEADERS_RECOMENDADOS if h not in headers]

        for i, h in enumerate(presentes):
            if i == len(presentes) - 1:
                print_end_item(f"✓ {h}")
            else:
                print_item(f"✓ {h}")
        for i, h in enumerate(ausentes):
            if i == len(ausentes) - 1:
                print_end_item(f"✗ {h} (MISSING)\n")
            else:
                print_item(f"✗ {h} (MISSING)")

        print_data(f"CORS")
        print_end_item(f"Status: {cors_status}\n")

        print_data(f"Cookies")
        if cookies:
            for i, c in enumerate(cookies):
                if i == len(cookies) - 1:
                    print_end_item(f"{c}\n")
                else:
                    print_item(f"{c}")
        else:
            print_end_item("Nenhum cookie encontrado.\n")

        print_data(f"Forms detect: {len(forms)}")
        if not forms:
            print_end_item("Nenhum formulário encontrado.\n")
        else:
            print_item(f"Forms encontrados: {len(forms)}")
            for i, form in enumerate(forms):
                is_last_form = i == len(forms) - 1
                print_item(f"Método: {form['method']} | Action: {form['action']}")
                for j, campo in enumerate(form['inputs']):
                    is_last_campo = j == len(form['inputs']) - 1
                    tipo = "[HIDDEN]" if campo['type'].lower() == 'hidden' else "Campo"
                    if is_last_form and is_last_campo:
                        print_sub_item_esc(f"{tipo} - Nome: {campo['name']} | Valor: {campo['value']}\n")
                    else:
                        print_item_c_esc(f"{tipo} - Nome: {campo['name']} | Valor: {campo['value']}")

        print_links_tree(url, max_depth=2)

        # Parâmetros
        print_data("Parâmetros URL principal:")
        for p in get_params([url]):
            print_item(p)

        print_item("Parâmetros links internos:")
        for i, p in enumerate(get_params(internal_links)):
            if i == len(get_params(internal_links)) - 1:
                print_sub_item_esc(p)
            else:
                print_item_c_esc(p)

        print_end_item("Parâmetros links externos:")
        for i, p in enumerate(get_params(external_links)):
            if i == len(get_params(external_links)) - 1:
                print_end_item_esc(f"{p}\n")
            else:
                print_item_esc(f"{p}")

        # Tecnologias
        print_data("Tecnologias detectadas:")
        tecnologias_keys = list(tecnologias.keys())
        for i, k in enumerate(tecnologias_keys):
            v = tecnologias[k]
            is_last_key = i == len(tecnologias_keys) - 1
            if isinstance(v, list):
                if is_last_key:
                    print_end_item(f"{k}:")
                else:
                    print_sub_item(f"{k}:")
                for j, item in enumerate(v):
                    is_last_item = j == len(v) - 1
                    if is_last_key and is_last_item:
                        print_end_item_esc(f"{item}\n")
                    elif is_last_item:
                        print_sub_item_esc(f"{item}\n")
                    else:
                        print_item(f"{item}\n")
            else:
                if is_last_key:
                    print_end_item(f"{k}: {v}\n")
                else:
                    print_sub_item(f"{k}: {v}")

        print_alert("SCAN COMPLETED | LOGGED")

    except Exception as e:
        print(f"Erro na verificação da URL: {e}")
        logging.error(f"Erro na verificação: {e}")

def run(user_args=None):
    parser = argparse.ArgumentParser(description="Scanner geral")
    parser.add_argument("-u", "--url", required=True, help="URL do alvo")
    parser.add_argument("--log", action="store_true", help="Adiciona log")
    args = parser.parse_args(user_args)

    """Verifica se o host está bloqueado"""
    parsed = urlparse(args.url)
    domain = parsed.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    for k in host:
        if domain == k or domain.endswith("." + k):
            print_alert("Host bloqueado por motivos de segurança.")
            logging.error(f"Host {domain} esta bloqueado por motivos de segurança.")
            return

    main(args.url, args)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Erro na execução do scanner: {e}")
        logging.error(f"Erro na execução do scanner: {e}")