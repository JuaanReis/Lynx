from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
import argparse
import copy
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from src.utils.file_utils import load_payloads, setup_logs

init(autoreset=True)

setup_logs()

def get_args_from_list(arg_list):
    parser = argparse.ArgumentParser(description="Ferramenta de XSS")
    parser.add_argument("--url", help="URL do alvo", required=True)
    parser.add_argument("--type", help="Tipo de ataque", choices=["armazenado", "refletido"], required=True)
    parser.add_argument("--payload", help="Arquivo de payloads", default="xss.txt")
    parser.add_argument("-l", type=int, help="Limitar a quantidade de payloads", default=None)
    parser.add_argument("--post", help="URL para envio do payload no XSS armazenado")
    parser.add_argument("--view", help="URL para ver resultado do XSS armazenado")
    parser.add_argument("-t", type=int, default=10, help="Número de threads")
    return parser.parse_args(arg_list)

def build_url(parsed_url, new_query):
    scheme = parsed_url.scheme if "localhost" not in parsed_url.netloc else ""
    netloc = "" if "localhost" in parsed_url.netloc else parsed_url.netloc
    path = parsed_url.path
    return urlunparse((scheme, netloc, path, parsed_url.params, new_query, parsed_url.fragment)).lstrip("/")

def payload_exe(payload, html):
    dangerous_contexts = [
        r'<script[^>]*>.*?' + re.escape(payload) + r'.*?</script>',
        r'on\w+\s*=\s*["\'].*?' + re.escape(payload) + r'.*?["\']',
        r'src\s*=\s*["\'].*?' + re.escape(payload) + r'.*?["\']',
        r'javascript:\s*' + re.escape(payload),
        re.escape(payload)
    ]
    for pattern in dangerous_contexts:
        if re.search(pattern, html, re.IGNORECASE | re.DOTALL):
            return True
    return False

def extrair_campos_formulario(form):
    campos = {}
    for inp in form.find_all("input"):
        tipo = inp.get("type", "text").lower()
        nome = inp.get("name")
        if nome and tipo in ["text", "search", "hidden", "email", "url"]:
            campos[nome] = ""
    for txt in form.find_all("textarea"):
        nome = txt.get("name")
        if nome:
            campos[nome] = ""
    return campos

def exibir_resultados(resultados, limite=None):
    print(f"{Fore.YELLOW}[!] " + f"{Fore.WHITE} Resultados do Scanner")
    if resultados:
        for i, (payload, url) in enumerate(resultados):
            print(f"{Fore.GREEN}[+] Refletido: {payload} --> {url}")
            if limite and i + 1 >= limite:
                print(Fore.MAGENTA + f"[!] " + f"{Fore.WHITE} Parado após encontrar {limite} XSS (limite definido pelo usuário).")
                break
    else:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum XSS detectado.")
def testar_payload_stored(payload, campos, post_url, view_url):
    try:
        data = campos.copy()
        for k in data:
            data[k] = payload

        requests.post(post_url, data=data, timeout=10)
        view = requests.get(view_url, timeout=10)

        if payload in view.text:
            return (payload, True)
        else:
            return (payload, False)
    except Exception as e:
        return (payload, f"Erro: {e}")

def scan_stored_xss(payloads, args):
    print(f"{Fore.CYAN}[~]" + f"{Fore.WHITE} Iniciando XSS armazenado (modo automático com threads)")
    try:
        res = requests.get(args.post, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.find("form")
        if not form:
            print(f"{Fore.RED}[-]" f"{Fore.WHITE} Nenhum formulário encontrado.")
            return

        campos = extrair_campos_formulario(form)
        print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Campos detectados: {list(campos.keys())}")

        resultados = []

        with ThreadPoolExecutor(max_workers=args.t) as executor:
            futures = [executor.submit(testar_payload_stored, payload, campos, args.post, args.view) for payload in payloads]

            for future in tqdm(as_completed(futures), total=len(futures), desc="Testando payloads"):
                payload_result = future.result()
                if isinstance(payload_result[1], bool) and payload_result[1]:
                    resultados.append(payload_result[0])

        print(f"\n{Fore.YELLOW}[!]" + f"{Fore.WHITE} Resultados do Scanner Armazenado")
        if resultados:
            for payload in resultados:
                print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} XSS armazenado DETECTADO: {payload}")
            print(f"{Fore.MAGENTA}[✓]" + f"{Fore.WHITE} Total de payloads bem-sucedidos: {len(resultados)}")
        else:
            print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum XSS armazenado detectado.")

    except Exception as e:
        print(f"{Fore.RED}[!]" + f"{Fore.WHITE} Falha ao configurar o ataque: {e}")

def testar_payload(payload, key, parsed_url, params):
    try:
        test_param = copy.deepcopy(params)
        test_param[key] = [payload]
        new_query = urlencode(test_param, doseq=True)
        full_url = build_url(parsed_url, new_query)
        response = requests.get(full_url, timeout=10)

        if payload in response.text and payload_exe(payload, response.text):
            return (payload, full_url)
    except Exception as e:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Requisição falhou: {e}")
    return None

def scan_reflect_xss(payloads, args):
    resultados = []
    parsed_url = urlparse(args.url)
    params = parse_qs(parsed_url.query)

    if not params:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Esse link não tem parâmetros para testar.")
        return

    print(f"{Fore.CYAN}[~]" + f"{Fore.WHITE} Parâmetros encontrados: {params}")
    print(f"{Fore.CYAN}[~]" + f"{Fore.WHITE} Iniciando XSS refletido com {args.t} threads")

    with ThreadPoolExecutor(max_workers=args.t) as executor:
        futures = []
        for payload in payloads:
            for key in params:
                futures.append(executor.submit(testar_payload, payload, key, parsed_url, params))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Testando payloads"):
            resultado = future.result()
            if resultado:
                resultados.append(resultado)

    exibir_resultados(resultados)

def main(args):
    logging.info(f"Executando o scanner de XSS com os seguintes parâmetros: {args}")
    logging.info(f"Payloads carregados: {args.payload}")
    logging.info(f"Tipo de ataque: {args.type}")
    logging.info(f"URL alvo: {args.url}")
    logging.info(f"Limite de payloads: {args.l}")
    logging.info(f"Threads: {args.t}")
    
    all_payloads = load_payloads(args.payload)
    payloads = all_payloads[:args.l] if args.l else all_payloads
    print(f"{Fore.MAGENTA}[*]" + f"{Fore.WHITE} Total de payloads carregados: {len(payloads)}")

    if args.type == "armazenado":
        if not args.post or not args.view:
            print(f"{Fore.RED}[!]" + f"{Fore.WHITE} Você precisa fornecer --post e --view para o modo armazenado")
            exit(1)
        scan_stored_xss(payloads, args)
    elif args.type == "refletido":
        scan_reflect_xss(payloads, args)

def run(user_args):
    try:
        args = get_args_from_list(user_args)
        main(args)
    except KeyboardInterrupt:
        print(f"{Fore.WHITE} \n[!]" + f"{Fore.WHITE} Scan interrompido pelo usuário.")
    except Exception as e:
        print(f"{Fore.WHITE} [ERRO]" + f"{Fore.WHITE} Algo deu ruim: " + str(e))