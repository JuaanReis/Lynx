import argparse
from src.utils.prints import print_data, print_alert, print_item, print_end_item
from .checkpath import check_path, found_path
from src.utils.file_utils import load_payloads
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from tqdm import tqdm
from src.utils.config import load_host
from src.utils.file_logs import setup_logs
import random
import string
import requests
import logging

setup_logs()
host = load_host()
found_path.clear()

def gerar_path(size=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def run(user_args):
    parser = argparse.ArgumentParser(description="Scanner de diretórios do Lynx")
    parser.add_argument("-u", "--url", help="URL alvo do teste", required=True)
    parser.add_argument("-w", help="Tipo de wordlist Ex:Admin ", default="path.txt")
    parser.add_argument("-l", type=int, help="Limite de caminhos a testar", default=5000)
    parser.add_argument("-t", type=int, help="Número de threads", default=10)
    parser.add_argument("-s", "--status", type=int, nargs="+", default=[200], help="Códigos HTTP válidos")
    parser.add_argument("-d", type=float, nargs=2, metavar=('MIN', 'MAX'), help="Delay entre requisições", default=(0.3, 0.5))
    parser.add_argument("-m", "--mode", choices=["normal", "debug"], default="normal", help="Modo de operação")

    args = parser.parse_args(user_args)

    path_f = gerar_path(16)
    url_fake = args.url.rstrip("/") + "/" + path_f
    try:
        response_fake = requests.get(url_fake, timeout=10)
        fake_body = response_fake.text
    except Exception as e:
        print_alert(f"Erro ao obter resposta fake {e}")
        fake_body = None

    parsed = urlparse(args.url)
    domain = parsed.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    for k in host:
        if domain == k or domain.endswith("." + k):
            print_alert(f"Host {domain} bloqueado por motivos de segurança.")
            logging.error(f"Host {domain} esta bloqueado por motivos de segurança.")
            return

    """Limite de caminhos pro modo admin"""
    if args.w == "admin":
        args.w = "admin_paths.txt"
        if args.l > 1000:
            print_alert("Ajustando o limite de 1000 caminhos para admin.")
            args.l = 1000
    else:
        args.w = "path.txt"
    """Carrega a wordlist"""
    payloads = load_payloads(args.w)


    """Limite de payloads"""
    if args.l >= 100000:
        res = input("[!!] Isso pode ferrar o servidor. Continuar mesmo assim? (Y/N): ").strip().lower()
        if res != 'y':
            print_alert("Limitando para 10000 paths.")
            args.l = 10000
        else:
            print_alert("Enviando 100k+ paths.")

    payloads = payloads[:args.l]

    print()
    print_data("Iniciando varredura de diretórios...")
    logging.info(f"Executando o scanner de diretórios com os seguintes parâmetros: {args}")
    print()
    print_data(f"Target: {args.url}")
    logging.info(f"URL alvo: {args.url}")
    print_item(f"Wordlist: {args.w}")
    logging.info(f"Wordlist: {args.w}")
    print_item(f"Total paths: {len(payloads)}")
    logging.info(f"Total de paths: {len(payloads)}")
    print_item(f"Threads: {args.t}")
    logging.info(f"Threads: {args.t}")
    print_item(f"Delay: {args.d}")
    logging.info(f"Delay: {args.d}")
    print_item(f"Valid stats: {args.status}")
    logging.info(f"Status válidos: {args.status}")
    print_end_item(f"Mode: {args.mode.capitalize()}")
    logging.info(f"Modo: {args.mode.capitalize()}")
    print()

    start_time = datetime.now()

    try:
        with ThreadPoolExecutor(max_workers=args.t) as executor:
            list(tqdm(
                executor.map(lambda p: check_path(p, args.url, args.status, args.d, args.mode, fake_body), payloads),
                total=len(payloads),
                desc="Testando caminhos",
                ncols=100
            ))
    except KeyboardInterrupt:
        print_alert("Scan interrompido pelo usuário.")
        logging.error("Scan interrompido pelo usuário.")
        return "Scan interrompido pelo usuário."

    """Calcula o tempo total de execução"""
    duration = datetime.now() - start_time

    print()
    print_data("Scan finalizado.")
    print_item(f"Diretorios encontrados: {len(found_path)}")
    logging.info(f"Diretórios encontrados: {len(found_path)}")
    print_end_item(f"Tempo total: {str(duration).split('.')[0]}")
    logging.info(f"Tempo total: {str(duration).split('.')[0]}")
    print()

    if found_path:
        logging.info("Caminhos encontrados:")
        if args.mode == "debug":
            for i, (url, status) in enumerate(found_path):
                if i == len(found_path) - 1:
                    print_end_item(f"[{status}] {url}")
                else:
                    print_item(f"[{status}] {url}")
                    logging.info(f"[{status}] {url}")
        else:
            print_data(f"Um total de {len(found_path)} caminhos foram encontrados")
    else:
        print_alert("Nenhum caminho válido foi encontrado.")
        logging.info("Nenhum caminho válido foi encontrado.")