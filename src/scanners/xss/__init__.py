import argparse
from colorama import Fore, init
from urllib.parse import urlparse
import logging
from src.utils.file_utils import load_payloads
from .reflected import scan_reflect_xss
from .stored import scan_stored_xss
from src.utils.config import load_host

init(autoreset=True)
host = load_host()

#Receber as flags do argparse 
def get_args_from_list(arg_list):
    parser = argparse.ArgumentParser(description="Ferramenta de XSS")
    parser.add_argument("--url", help="URL do alvo", default="None")
    parser.add_argument("--type", help="Tipo de ataque", choices=["armazenado", "refletido"], required=True)
    parser.add_argument("--payload", help="Arquivo de payloads", default="xss.txt")
    parser.add_argument("-l", type=int, help="Limitar a quantidade de payloads", default=None)
    parser.add_argument("--post", help="URL para envio do payload no XSS armazenado")
    parser.add_argument("--view", help="URL para ver resultado do XSS armazenado")
    parser.add_argument("-t", type=int, default=10, help="Número de threads")
    return parser.parse_args(arg_list)

#Main
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
        parsed = urlparse(args.url)
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        for k in host:
            if domain == k or domain.endswith("." + k):
                print(f"{Fore.RED}[!]" + f"{Fore.WHITE} Host {domain} esta bloqueado por motivos de segurança.")
                logging.info(f"URL testada: {args.url}")
                logging.error(f"Host {domain} esta bloqueado por motivos de segurança.")
                return
        main(args)
    except KeyboardInterrupt:
        print(f"{Fore.RED} \n[!]" + f"{Fore.WHITE} Scan interrompido pelo usuário.")
    except Exception as e:
        print(f"{Fore.RED} [ERRO]" + f"{Fore.WHITE} Algo deu ruim: " + str(e))
        logging.error(f"Erro: {e}")