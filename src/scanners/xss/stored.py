import requests
from colorama import Fore, init
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils import testar_payload_stored, extrair_campos_formulario

init(autoreset=True)

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