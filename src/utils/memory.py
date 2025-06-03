import os
import psutil
import sys
from colorama import Fore, init

init(autoreset=True)

def check_memory_limit(limit_mb):
    #Verifica o uso de memória atual do processo e compara com o limite (em MB). Se o uso de memória exceder o limite, o processo é finalizado.

    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Converte de bytes para MB

    if memory_usage > limit_mb:
        print(f"{Fore.WHITE} [!]" + f"{Fore.WHITE} Uso de memória excedeu o limite de {limit_mb}MB. Usando {memory_usage:.2f}MB. Abortando...\n")
        sys.exit(1)  # Finaliza o programa, você pode escolher outra ação como liberar memória ou algo mais
    else:
        print(f"{Fore.GREEN} [+]" + f"{Fore.WHITE} Memória usada: {memory_usage:.2f}MB (dentro do limite)\n")
