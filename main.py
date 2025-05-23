import shlex
from colorama import Fore, Style, init
import time
import random
import socket
import platform
from tqdm import tqdm
from src.core.check_memory import check_memory_limit
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

    print(f"{Fore.CYAN}[*]" + f"{Fore.WHITE} Ferramenta de testes para varredura e exploração web para pesquisadores de segurança.")
    print(f"{Fore.YELLOW}[!]" + f"{Fore.WHITE} USO RESPONSÁVEL OBRIGATÓRIO!")
    print(f"{Fore.RED} [!]" + f"{Fore.WHITE} Essa ferramenta é destinada apenas para testes autorizados e ambientes controlados.")
    print(f"{Fore.RED} [!]" + f"{Fore.WHITE} O autor não se responsabiliza por qualquer uso indevido desta aplicação.\n")
    print(f"{Fore.MAGENTA}[*]" + f"{Fore.WHITE} Contato: pinguim.secreto@gmail.com")
    print(f"{Fore.BLUE}[!]" + f"{Fore.WHITE} Site oficial (em breve): https://lynxsec.io\n")

def menu_principal():
    print(f"{Fore.CYAN} [*]" + f"{Fore.WHITE} Selecione uma das ferramentas disponíveis:\n")
    print(f"{Fore.BLUE}[1]" + f"{Fore.WHITE} Scanner de XSS")
    print(f"{Fore.BLUE}[2]" + f"{Fore.WHITE} Scanner de Caminhos")
    print(f"{Fore.BLUE}[3]" + f"{Fore.WHITE} Ataques de Força Bruta")
    print(f"{Fore.BLUE}[4]" + f"{Fore.WHITE} Scanner de SMAP" + f"{Fore.CYAN} (Sistema de Mapas de Arquivos)")
    print(f"{Fore.RED}[0]" + f"{Fore.WHITE} Sair\n")

def system_info():
    print(f"{Fore.CYAN}[*]{Fore.WHITE} Sistema Operacional: {platform.system()} {platform.release()}")
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        ip = "IP não disponível"
    print(f"{Fore.CYAN}[*]" + f"{Fore.WHITE} IP Local: {ip}")
    if conectado:
        print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} Conectado à Internet com ping de {ping} ms")
    else:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Sem conexão com a Internet. Verifique sua rede.")

def godmode():
    mensagens = [
        "Iniciando varredura em tempo real",
        "Conectando ao servidor remoto",
        "Desenvolvendo exploit de zero day",
        "Explorando vulnerabilidades de SQLi",
        "Acesso root garantido!",
        "Desmontando segurança do sistema",
        "Injetando payload em todos os servidores",
        "Download completo. Prepare-se para o caos"
    ]

    for msg in mensagens:
        for i in tqdm(range(100), desc=msg, ncols=80, bar_format="{l_bar}{bar} | {percentage:3.0f}%"):
            time.sleep(random.uniform(0.07, 0.09))  # Tempo entre as atualizações de barra de progresso

        # Agora mostra a próxima mensagem com um pequeno delay para aumentar o drama
        time.sleep(1)

    print(f"{Fore.YELLOW}[!]" + f"{Fore.WHITE} Acesso administrativo concedido...")
    time.sleep(1)
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro fatal por favor aguarde um instante")
    time.sleep(1.5)
    print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro não localizado")
    return

def main():
    # Exibe banner inicial
    exibe_banner()
    system_info()

    # Modo de operação
    if OPERATION_MODE == "test":
        print(f"{Fore.YELLOW}[!]" + f"{Fore.WHITE} A ferramenta está em modo de teste. Algumas funcionalidades podem ser limitadas.{Style.RESET_ALL}\n")

    # Loop principal de interação
    while True:
        # Verifica o uso de memória antes de cada operação importante
        check_memory_limit(MEMORY_LIMIT)

        menu_principal()
        escolha = input(f"{Fore.GREEN}[!]" + f"{Fore.WHITE} Digite o número da opção desejada: ").strip()

        if escolha == "1":
            from src.scanners import xss
            print(f"{Fore.MAGENTA}[MODO XSS]{Style.RESET_ALL} Insira os argumentos para execução do scanner de XSS:")
            user_input = input(f"{Fore.GREEN}> ")
            user_args = shlex.split(user_input)
            xss.run(user_args)

        elif escolha == "2":
            from src.scanners import path
            print(f"{Fore.MAGENTA}[MODO PATH]{Style.RESET_ALL} Insira os argumentos para execução do scanner de diretórios:")
            user_input = input(f"{Fore.GREEN}> ")
            user_args = shlex.split(user_input)
            path.run(user_args)

        elif escolha == "3":
            from src.scanners.bruteForce import brute
            print(f"{Fore.MAGENTA}[MODO BRUTE FORCE]{Style.RESET_ALL} Insira os argumentos para iniciar a força bruta:")
            user_input = input(f"{Fore.GREEN}> ")
            user_args = shlex.split(user_input)
            brute.run(user_args)

        elif escolha == "4":
            from src.scanners import smap
            print(f"{Fore.MAGENTA}[INFO]" + f"{Fore.WHITE} Informações sobre o site:")
            user_input = input(f"{Fore.GREEN}> ")
            user_args = shlex.split(user_input)
            smap.run(user_args)

        elif escolha == "godmode":
            godmode()

        elif escolha == "0":
            print(f"{Fore.RED}{Style.BRIGHT}Encerrando..." + f"{Fore.WHITE} Obrigado por utilizar o LYNX.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Opção inválida." + f"{Fore.WHITE} Tenta de novo, hacker wannabe! Isso não é tão fácil assim, vai por mim.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED} \n[!]" + f"{Fore.WHITE} Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"{Fore.RED} [ERRO]" + f"{Fore.WHITE} Algo deu ruim: " + str(e))