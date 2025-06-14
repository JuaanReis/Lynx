from urllib.parse import urlparse, parse_qs
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from src.utils.file_logs import setup_logs
from .test_payload import testar_payload
from .result import exibir_resultados
from src.utils.prints import print_data, print_alert, print_item, print_end_item
import logging

setup_logs()

init(autoreset=True)

def scan_reflect_xss(payloads, args):
    try:
        resultados = []
        parsed_url = urlparse(args.url)
        params = parse_qs(parsed_url.query)

        if not params:
            print_alert("Esse link não tem parâmetros para testar.")
            logging.error(f"Esse link não tem parâmetros para testar.")
            return

        print_data(f"Parâmetros encontrados: {len(params)}")
        for i, item in enumerate(params):
            if i == len(params) -1:
                print_end_item(f" Parâmetro: {item} | Valor: {params[item]}\n")      
            else:
                print_item(f" Parâmetro: {item} | Valor: {params[item]}")

        with ThreadPoolExecutor(max_workers=args.thread) as executor:
            futures = []
            for payload in payloads:
                for key in params:
                    futures.append(executor.submit(testar_payload, payload, key, parsed_url, params))

            for future in tqdm(as_completed(futures), total=len(futures), desc="Testing payloads"):
                resultado = future.result()
                if resultado:
                    resultados.append(resultado)
        print()
        exibir_resultados(resultados, args)
    except Exception as e:
        print_alert(f"Erro ao executar o scanner de XSS refletido: {e}")
        logging.error(f"Erro ao executar o scanner de XSS refletido: {e}")