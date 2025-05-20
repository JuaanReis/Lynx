import argparse
from colorama import Fore, Style, init
from .color import print_color
from .checkpath import check_path, found_path
from src.utils.file_utils import load_payloads
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from tqdm import tqdm
from src.utils.config import load_host
from src.utils.file_logs import setup_logs
import logging

init(autoreset=True)


setup_logs()
found_path.clear()
host = load_host()

def run(user_args):
    parser = argparse.ArgumentParser(description="Scanner de diretórios do Nexor")
    parser.add_argument("-u", "--url", help="URL alvo do teste", required=True)
    parser.add_argument("-w", help="Caminho do arquivo txt com os paths", default="path.txt")
    parser.add_argument("-l", type=int, help="Limite de caminhos a testar", default=5000)
    parser.add_argument("-t", type=int, help="Número de threads", default=10)
    parser.add_argument("-s", "--status", type=int, nargs="+", default=[200], help="Códigos HTTP válidos")
    parser.add_argument("-d", type=float, nargs=2, metavar=('MIN', 'MAX'), help="Delay entre requisições", default=(0, 0))
    parser.add_argument("-m", "--mode", choices=["normal", "debug"], default="normal", help="Modo de operação")

    args = parser.parse_args(user_args)

    parsed = urlparse(args.url)
    domain = parsed.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    for k in host:
        if domain == k or domain.endswith("." + k):
            print_color("!", "Host bloqueado por motivos de segurança.", Fore.RED)
            logging.error(f"Host {domain} esta bloqueado por motivos de segurança.")
            return

    if args.t > 50:
        res = input(Fore.YELLOW + "[!] Mais de 50 threads pode travar tudo. Continuar? (Y/N): ").strip().lower()
        if res != 'y':
            print_color("!", "Limitando para 50 threads.", Fore.YELLOW)
            args.t = 50

    payloads = load_payloads(args.w)

    if args.l >= 100000:
        res = input(Fore.RED + "[!] Isso pode ferrar o servidor. Continuar mesmo assim? (Y/N): ").strip().lower()
        if res != 'y':
            print_color("+", "Limitando para 10000 paths.", Fore.GREEN)
            args.l = 10000
        else:
            print_color("!", "Enviando 100k+ paths. GG pro servidor.", Fore.YELLOW)

    payloads = payloads[:args.l]

    print()
    print_color("+", "Iniciando varredura de diretórios...", Fore.GREEN)
    logging.info(f"Executando o scanner de diretórios com os seguintes parâmetros: {args}")
    print()
    print_color("+", f"Alvo: {args.url}", Fore.GREEN)
    logging.info(f"URL alvo: {args.url}")
    print_color("+", f"Wordlist: {args.w}", Fore.GREEN)
    logging.info(f"Wordlist: {args.w}")
    print_color("+", f"Total de paths: {len(payloads)}", Fore.GREEN)
    logging.info(f"Total de paths: {len(payloads)}")
    print_color("+", f"Threads: {args.t}", Fore.GREEN)
    logging.info(f"Threads: {args.t}")
    print_color("+", f"Status válidos: {args.status}", Fore.GREEN)
    logging.info(f"Status válidos: {args.status}")
    print_color("+", f"Modo: {args.mode.capitalize()}", Fore.GREEN)
    logging.info(f"Modo: {args.mode.capitalize()}")
    print()

    start_time = datetime.now()

    try:
        with ThreadPoolExecutor(max_workers=args.t) as executor:
            list(tqdm(
                executor.map(lambda p: check_path(p, args.url, args.status, args.d, args.mode), payloads),
                total=len(payloads),
                desc="[+] Testando caminhos",
                ncols=100
            ))
    except KeyboardInterrupt:
        print_color("!", "Scan interrompido pelo usuário.", Fore.YELLOW)
        logging.error("Scan interrompido pelo usuário.")
        return "!", "Scan interrompido pelo usuário."

    duration = datetime.now() - start_time

    print()
    print_color("+", "Scan finalizado.", Fore.GREEN)
    logging.info("Scan finalizado.")
    print_color("+", f"Diretórios encontrados: {len(found_path)}", Fore.GREEN)
    logging.info(f"Diretórios encontrados: {len(found_path)}")
    print_color("+", f"Tempo total: {str(duration).split('.')[0]}", Fore.GREEN)
    logging.info(f"Tempo total: {str(duration).split('.')[0]}")
    print()

    if found_path:
        print_color("+", "Caminhos válidos encontrados:", Fore.GREEN)
        logging.info("Caminhos válidos encontrados:")
        for url, status in found_path:
            print(f"{Fore.BLUE}[{status}]{Style.RESET_ALL} {url}")
            logging.info(f"[{status}] {url}")
    else:
        print_color("-", "Nenhum caminho válido foi encontrado.", Fore.RED)
        logging.info("Nenhum caminho válido foi encontrado.")