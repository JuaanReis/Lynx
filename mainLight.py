from colorama import Fore, init
from settings import DEV_MODE_MESSAGE, DEV_MODE, LEGAL_USE_ONLY, ALERT_MESSAGE
import shlex

init(autoreset=True)

if DEV_MODE:
    print(f"{Fore.YELLOW}{DEV_MODE_MESSAGE}")
if LEGAL_USE_ONLY:
    print(f"{Fore.RED}{ALERT_MESSAGE}")

def menu():
    print(f"{Fore.CYAN}[*]" + f"{Fore.WHITE} Ferramentas disponíveis:\n")
    print(f"{Fore.BLUE}[1]" + f"{Fore.WHITE} Scanner de XSS")
    print(f"{Fore.BLUE}[2]" + f"{Fore.WHITE} Scanner de Caminhos")
    print(f"{Fore.BLUE}[3]" + f"{Fore.WHITE} Scanner de SMAP" + f"{Fore.CYAN} (Sistema de Mapas de Arquivos)")
    print(f"{Fore.RED}[0]" + f"{Fore.WHITE} Sair\n")

def main():
  menu()

  while True:
    escolha = input(f"{Fore.CYAN}[*]" + f"{Fore.WHITE} Escolha uma opção: ")

    if escolha == "1":
        from src.scanners import xss
        print(f"{Fore.BLUE}[XSS MODE]" + f"{Fore.WHITE} insira os argumentos para o scanner de XSS:")
        user_input = input(f"{Fore.GREEN}> ")
        user_args = shlex.split(user_input)
        xss.run(user_args)

    elif escolha == "2":
        from src.scanners import path
        print(f"{Fore.BLUE}[PATH MODE]" + f"{Fore.WHITE} insira os argumentos para o scanner de Caminhos:")
        user_input = input(f"{Fore.GREEN}> ")
        user_args = shlex.split(user_input)
        path.run(user_args)

    elif escolha == "3":
        from src.scanners import smap
        print(f"{Fore.BLUE}[SMAP MODE]" + f"{Fore.WHITE} insira os argumentos para o scanner de SMAP:")
        user_input = input(f"{Fore.GREEN}> ")
        user_args = shlex.split(user_input)
        smap.run(user_args)

    elif escolha == "0":
        print(f"{Fore.RED}[!] Saindo...")
        import sys
        sys.exit(0)
    else:
        print(f"{Fore.RED}[!] Opção inválida. Tente novamente.")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}[!] Interrompido pelo usuário.")
    except Exception as e:
        print(f"{Fore.RED}[!] Erro inesperado: {e}")
