from colorama import Fore, init

init(autoreset=True)

def exibir_resultados(resultados, args):
    print(f"{Fore.YELLOW}[!] " + f"{Fore.WHITE} Resultados do Scanner")
    if resultados:
            if args.debug:
                for i, (payload, url) in enumerate(resultados):
                    print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} XSS detectado: Refletido:" + f"{Fore.YELLOW} {payload}  " + f"{Fore.WHITE}->  na URL: {url}")
            else:
                print(f"{Fore.MAGENTA}[✓]" + f"{Fore.WHITE} Total de payloads bem-sucedidos: {len(resultados)}")
    else:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum XSS detectado.")