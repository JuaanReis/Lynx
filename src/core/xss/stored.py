import requests
from colorama import Fore, init
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from .testar_payload_stored import testar_payload_stored
from .form import extrair_campos_formulario
from src.utils.prints import print_alert, print_data, print_item, print_end_item

init(autoreset=True)

def scan_stored_xss(payloads, args):
    try:
        res = requests.get(args.post, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.find("form")
        if not form:
            print_alert(f" Nenhum formulário encontrado.")
            return

        campos = extrair_campos_formulario(form)
        for i, (campo, tipo) in enumerate(campos.items()):
            if i == len(campos) - 1:
                print_end_item(f" Campo: {campo} | Tipo: {tipo}\n")
            else:
                print_item(f" Campo: {campo} | Tipo: {tipo}")

        resultados = []

        with ThreadPoolExecutor(max_workers=args.thread) as executor:
            futures = [executor.submit(testar_payload_stored, payload, campos, args.post, args.view) for payload in payloads]

            for future in tqdm(as_completed(futures), total=len(futures), desc="Testando payloads"):
                payload_result = future.result()
                if isinstance(payload_result[1], bool) and payload_result[1]:
                    resultados.append(payload_result[0])
        print() # Quebra de linha

        print_data(f" Resultados do Scanner Armazenado")
        if resultados:
            if args.debug:
                for i, payload in enumerate(resultados):
                    if i == len(resultados) - 1:
                        print_end_item(f"{Fore.MAGENTA}[{i+1}]" + f"{Fore.WHITE} Payload: {payload}")
                    else:
                        print_item(f"{Fore.MAGENTA}[{i+1}]" + f"{Fore.WHITE} Payload: {payload}")
            else:
                print_data(f"{Fore.WHITE} Total de payloads bem-sucedidos: {len(resultados)}")
        else:
            print(f"{Fore.WHITE} Nenhum XSS armazenado detectado.")

    except Exception as e:
        print_alert(f"Falha ao configurar o ataque: {e}")