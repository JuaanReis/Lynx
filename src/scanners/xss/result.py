from colorama import Fore, init
from src.utils.prints import print_data, print_alert, print_item, print_end_item
import requests

init(autoreset=True)

def exibir_resultados(resultados, args):
    try:
        print_data("Resultados do Scanner\n")
        if resultados:
                if args.debug:
                    for i, (payload, url) in enumerate(resultados):
                        if i == len(resultados) - 1:
                            try:
                                response = requests.get(url, timeout=5)
                                status = response.status_code
                            except Exception as e:
                                status = f"[ERRO]: {e}"
                            print_end_item(f"{Fore.MAGENTA}[{i+1}]" + f"{Fore.WHITE} Payload: {payload} | URL: {url} | Status: {status}")
                        else:
                            print_item(f"{Fore.MAGENTA}[{i+1}]" + f"{Fore.WHITE} Payload: {payload} | URL: {url}\n")
                else:
                    print_end_item(f"[{len(resultados)}] Total de XSS detectados: {len(resultados)}\n")
        else:
            print_alert(f" Nenhum XSS detectado.")
    except Exception as e:
        print_alert(f"Erro ao exibir resultados: {e}")