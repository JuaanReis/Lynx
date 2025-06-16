import shlex
from colorama import Fore, Style, init
import time
import sys
import socket
import platform
from src.utils.memory import check_memory_limit
from src.utils.ping import test_connection
from settings import OPERATION_MODE, LEGAL_USE_ONLY, ALERT_MESSAGE

init(autoreset=True)

MEMORY_LIMIT = 500  # Limite de 500MB

conectado, ping = test_connection()

def exibe_banner():
    print(f"{Fore.GREEN}{Style.BRIGHT}")
    print(f"{Fore.RED}" + r"""
     ██▓   ▓██   ██▓ ███▄    █ ▒██   ██▒
    ▓██▒    ▒██  ██▒ ██ ▀█   █ ▒▒ █ █ ▒░
    ▒██░     ▒██ ██░▓██  ▀█ ██▒░░  █ █ ▒
    ▒██░     ░ ▐██▓░▓██▒  ▐▌██▒ ░ █ █ ▒
    ░██████▒ ░ ██▒▓░▒██░   ▓██░▒██▒ ▒██▒
    ░ ▒░▓  ░  ██▒▒▒ ░ ▒░   ▒ ▒ ▒▒ ░ ░▓ ░
    ░ ░ ▒  ░▓██ ░▒░ ░ ░░   ░ ▒░░░   ░▒ ░
      ░ ░   ▒ ▒ ░░     ░   ░ ░  ░    ░
        ░  ░░ ░              ░  ░    ░
            ░ ░
         Web Security Suite 2025
        by Juan | Versão 1.0 (beta)
    """)

    # Verifica se a opção LEGAL_USE_ONLY está ativada
    if LEGAL_USE_ONLY:
        print(f"{Fore.RED}{ALERT_MESSAGE}{Style.RESET_ALL}")

    if OPERATION_MODE == "test":
        print(f"{Fore.YELLOW}[!]{Fore.WHITE} A ferramenta está em modo de teste. Algumas funcionalidades podem ser limitadas.{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}[#]{Fore.WHITE} Contato: 01pingu.noot@gmail.com")

def menu_principal():
    print(f"{Fore.CYAN}[*]{Fore.WHITE} Selecione uma das ferramentas disponíveis:\n")
    print(f"{Fore.BLUE}[1]{Fore.WHITE} Scanner de XSS")
    print(f"{Fore.BLUE}[2]{Fore.WHITE} Scanner de Caminhos")
    print(f"{Fore.BLUE}[3]{Fore.WHITE} Scanner de SMAP" + f"{Fore.CYAN} (Sistema de Mapas de Arquivos)")
    print(f"{Fore.RED}[0]{Fore.WHITE} Sair\n")

def system_info():
    try:
        if conectado:
            print(f"{Fore.GREEN}[+]{Fore.WHITE} Conectado à Internet com ping de {ping} ms")
        else:
            print(f"{Fore.RED}[-]{Fore.WHITE} Sem conexão com a Internet. Verifique sua rede.")
    except Exception as e:
        print(f"{Fore.RED}[ERRO]{Fore.WHITE} Ocorreu um erro ao verificar a conexão: {e}")

def main():
    exibe_banner()

    # Exibe banner inicial
    menu_principal()

    # Loop principal de interação
    while True:

        escolha = input(f"{Fore.GREEN}[!]{Fore.WHITE} Digite o número da opção desejada: ").strip()

        if escolha == "1":
            from src.core import xss
            print(f"{Fore.MAGENTA}[MODO XSS]{Style.RESET_ALL} Insira os argumentos para execução do scanner de XSS:")
            user_input = input(f"{Fore.GREEN}> {Fore.WHITE}")
            user_args = shlex.split(user_input)
            try:
                xss.run(user_args)
            except Exception as e:
                print(f"{Fore.RED}[ERRO]{Fore.WHITE} Ocorreu um erro com o scanner de XSS: {e}")

        elif escolha == "2":
            from src.core import path
            print(f"{Fore.MAGENTA}[MODO PATH]{Style.RESET_ALL} Insira os argumentos para execução do scanner de diretórios:")
            user_input = input(f"{Fore.GREEN}> {Fore.WHITE}")
            user_args = shlex.split(user_input)
            try:
                path.run(user_args)
            except Exception as e:
                print(f"{Fore.RED}[ERRO]{Fore.WHITE} Ocorreu um erro com o scanner de caminhos: {e}")

        elif escolha == "3":
            from src.core import smap
            print(f"{Fore.MAGENTA}[SMAP]{Fore.WHITE} Scanner de web sites:")
            user_input = input(f"{Fore.GREEN}> {Fore.WHITE}")
            user_args = shlex.split(user_input)
            try:
                smap.run(user_args)
            except Exception as e:
                print(f"{Fore.RED}[ERRO]{Fore.WHITE} Ocorreu um erro com o SMAP: {e}")

        elif escolha == "0":
            print(f"{Fore.RED}{Style.BRIGHT}Encerrando..." + f"{Fore.WHITE} Obrigado por utilizar o LYNX.{Style.RESET_ALL}")
            break

        elif escolha == " ":
            try:
                print(f"{Fore.YELLOW}[!]{Fore.WHITE} Escolha uma opção válida do menu.")
            except Exception as e:
                print(f"{Fore.RED}[ERRO]{Fore.WHITE} Ocorreu um erro ao processar sua escolha: {e}")

        else:
            print(f"{Fore.RED}Opção inválida." + f"{Fore.WHITE} Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED} \n[!]" + f"{Fore.WHITE} Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"{Fore.RED} [ERRO]" + f"{Fore.WHITE} Algo deu ruim: " + str(e))
        sys.exit(1)