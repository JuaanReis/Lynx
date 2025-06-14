import argparse
import sys
from colorama import Fore, init
from urllib.parse import urlparse
import logging
from src.utils.file_utils import load_payloads
from .block_host import block_host
from .logs import logs
from src.utils.config import load_host
from src.utils.prints import print_alert, print_data, print_hack

init(autoreset=True)
host = load_host()

#Receber as flags do argparse
def get_args_from_list(arg_list):
    parser = argparse.ArgumentParser(description="Ferramenta de XSS")
    parser.add_argument("--url", "-u", help="URL do alvo", default=None, action="store")
    parser.add_argument("--type", "-T", action="store", help="Tipo de ataque", choices=["armazenado", "refletido", "r", "a"], required=True)
    parser.add_argument("--payload", help="Arquivo de payloads", default="xss.txt")
    parser.add_argument("--limit", "-l", type=int, help="Limitar a quantidade de payloads", default=None)
    parser.add_argument("--post", "-p", help="URL para envio do payload no XSS armazenado")
    parser.add_argument("--view", "-v", help="URL para ver resultado do XSS armazenado")
    parser.add_argument("--thread", "-t", type=int, default=10, help="Número de threads")
    parser.add_argument("--debug", "-d", action="store_true", help="Ativar modo debug", default=False)
    return parser.parse_args(arg_list)

#Main
def main(args):
    """Exibe informações iniciais do scanner de XSS"""
    print_hack(f" Target: {args.url}")

    """Carrega os payloads do arquivo especificado"""
    all_payloads = load_payloads(args.payload)
    payloads = all_payloads[:args.limit] if args.limit else all_payloads
    print_data(f" Total de payloads carregados: {len(payloads)}")

    """Verifica o tipo de ataque e chama a função correspondente"""
    if args.type == "armazenado" or args.type  == "a":
        if not args.post or not args.view:
            print_alert(f"\n{Fore.WHITE} Você precisa fornecer --post e --view para o modo armazenado")
            sys.exit(1)
        from .stored import scan_stored_xss
        scan_stored_xss(payloads, args)

    elif args.type == "refletido" or args.type == "r":
        if not args.url:
            print_alert(f"\n Você precisa fornecer --url para o modo refletido")
            sys.exit(1)
        from .reflected import scan_reflect_xss
        scan_reflect_xss(payloads, args)

def run(user_args):
    try:
        args = get_args_from_list(user_args)

        """Bloqueia hosts não permitidos"""
        if block_host(args, host):
            sys.exit(1)

        """Registra logs de execução do scanner de XSS"""

        parsed = urlparse(args.url)
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]

        logs(args, domain)

        """Inicia o scanner de XSS"""
        main(args)

    except KeyboardInterrupt:
        print_alert(f"{Fore.WHITE} Scan interrompido pelo usuário.")
    except Exception as e:
        print_alert(f"{Fore.WHITE} Algo deu ruim: " + str(e))
        logging.error(f"Erro: {e}")