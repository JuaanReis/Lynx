from urllib.parse import urlparse, parse_qs
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from src.utils.file_logs import setup_logs
from .test_payload import testar_payload
from .result import exibir_resultados
import logging

setup_logs()

init(autoreset=True)

def scan_reflect_xss(payloads, args):
    resultados = []
    parsed_url = urlparse(args.url)
    params = parse_qs(parsed_url.query)

    if not params:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Esse link não tem parâmetros para testar.")
        logging.error(f"Esse link não tem parâmetros para testar.")
        return f"{Fore.RED}[-]" + f"{Fore.WHITE} Esse link não tem parâmetros para testar."

    print(f"{Fore.CYAN}[~]" + f"{Fore.WHITE} Parâmetros encontrados: {params}")
    print(f"{Fore.CYAN}[~]" + f"{Fore.WHITE} Iniciando XSS refletido com {args.thread} threads")

    with ThreadPoolExecutor(max_workers=args.thread) as executor:
        futures = []
        for payload in payloads:
            for key in params:
                futures.append(executor.submit(testar_payload, payload, key, parsed_url, params))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Testando payloads"):
            resultado = future.result()
            if resultado:
                resultados.append(resultado)
    exibir_resultados(resultados, args)