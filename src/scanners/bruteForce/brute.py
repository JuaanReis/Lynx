import argparse
import subprocess
import os
from colorama import Fore, init
from src.utils.file_utils import load_payloads

init(autoreset=True)

def run(user_args=None):
    parser = argparse.ArgumentParser(description="Força bruta com Nexor")
    parser.add_argument("-u", "--url", required=True, help="URL do login")
    parser.add_argument("--user", required=True, help="Usuário fixo para testar as senhas")
    parser.add_argument("--passlist", required=True, help="Arquivo com senhas")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Número de threads (padrão: 10)")
    args = parser.parse_args(user_args if user_args is not None else [])

    binary = "src/scanners/brute_bin"
    if not os.path.isfile(binary):
        print(Fore.RED + "[ERRO] Binário brute_bin não encontrado! Compile o brute.c com: gcc brute.c -o brute_bin -pthread")
        return

    print(Fore.CYAN + "[*] Iniciando força bruta...")
    print(Fore.CYAN + f"[*] Alvo: {args.url}")
    print(Fore.CYAN + f"[*] Usuário: {args.user} | Senhas: {args.passlist}")
    print(Fore.CYAN + f"[*] Threads: {args.threads}\n")

    # Carrega senhas e gera arquivo de combos temporário
    try:
        senhas = load_payloads(args.passlist)
        combo_file = "combo_temp.txt"
        with open(combo_file, "w") as f:
            for senha in senhas:
                f.write(f"{args.user}:{senha}\n")
    except Exception as e:
        print(Fore.RED + f"[ERRO] Falha ao preparar combos: {e}")
        return f"{Fore.RED}[-]" + f"{Fore.WHITE} Falha ao preparar combos: {e}"

    try:
        result = subprocess.run(
            [binary, args.url, combo_file, "Welcome", str(args.threads)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(Fore.GREEN + result.stdout)
        if result.stderr:
            print(Fore.RED + result.stderr)
    except Exception as e:
        print(Fore.RED + f"[ERRO] Falha ao executar o binário: {e}")
    finally:
        if os.path.exists(combo_file):
            os.remove(combo_file)