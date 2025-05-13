from src.utils.file_utils import load_payloads
import requests
import argparse
import time
import random
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from threading import Lock
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

found_path = []
lock = Lock()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

def print_color(label, msg, cor=Fore.WHITE):
    print(f"{cor}[{label}]{Style.RESET_ALL} {msg}")

def is_valid_response(response, valid_status):
    if response.status_code not in valid_status:
        return False
    content = response.text.lower()
    invalid_patterns = ["not found", "404", "não encontrado", "page not available"]
    return not any(p in content for p in invalid_patterns)

def check_path(path, base_url, valid_status, delay_range, mode):
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=False)

        if mode == "debug":
            print_color("DEBUG", f"Requisitando: {url} - Status: {response.status_code}")

        if is_valid_response(response, valid_status):
            with lock:
                found_path.append((url, response.status_code))
        elif response.status_code == 429:
            time.sleep(5)
            return check_path(path, base_url, valid_status, delay_range, mode)
    except requests.RequestException:
        pass

    if delay_range:
        time.sleep(random.uniform(*delay_range))

def run(user_args):
    parser = argparse.ArgumentParser(description="Scanner de diretórios do Nexor")
    parser.add_argument("--url", help="URL alvo do teste", required=True)
    parser.add_argument("-w", help="Caminho do arquivo txt com os paths", default="path.txt")
    parser.add_argument("-l", type=int, help="Limite de caminhos a testar", required=True)
    parser.add_argument("-t", type=int, help="Número de threads", default=10)
    parser.add_argument("--status", type=int, nargs="+", default=[200], help="Códigos HTTP válidos")
    parser.add_argument("-d", type=float, nargs=2, metavar=('MIN', 'MAX'), help="Delay entre requisições")
    parser.add_argument("--mode", choices=["debug", "legal", "operation"], default="operation", help="Modo de operação")

    args = parser.parse_args(user_args)

    if args.mode == "legal":
        print_color("ALERTA", "Uso da ferramenta é de responsabilidade do usuário. Use apenas para fins legais.", Fore.RED)
        input(Fore.YELLOW + "[!] Pressione Enter para continuar com o uso legal...")

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
    print()
    print_color("+", f"Alvo: {args.url}", Fore.GREEN)
    print_color("+", f"Wordlist: {args.w}", Fore.GREEN)
    print_color("+", f"Total de paths: {len(payloads)}", Fore.GREEN)
    print_color("+", f"Threads: {args.t}", Fore.GREEN)
    print_color("+", f"Status válidos: {args.status}", Fore.GREEN)
    print_color("+", f"Modo: {args.mode.capitalize()}", Fore.GREEN)
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
        return

    duration = datetime.now() - start_time

    print()
    print_color("+", "Scan finalizado.", Fore.GREEN)
    print_color("+", f"Diretórios encontrados: {len(found_path)}", Fore.GREEN)
    print_color("+", f"Tempo total: {str(duration).split('.')[0]}", Fore.GREEN)
    print()

    if found_path:
        print_color("+", "Caminhos válidos encontrados:", Fore.GREEN)
        for url, status in found_path:
            print(f"{Fore.BLUE}[{status}]{Style.RESET_ALL} {url}")
    else:
        print_color("-", "Nenhum caminho válido foi encontrado.", Fore.RED)
