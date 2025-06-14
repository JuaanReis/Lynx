from colorama import Fore, init
init(autoreset=True)

def print_data(label):
    try:
        print(f"{Fore.CYAN}[::]{Fore.WHITE} {label.upper()}")
    except Exception as e:
        print(f"Erro ao imprimir dados: {e}")

def print_alert(msg):
    try:
        print(f"{Fore.RED}[!!]{Fore.WHITE} {msg}")
    except Exception as e:
        print(f"Erro ao imprimir alerta: {e}")

def print_hack(msg):
    try:
        print(f"{Fore.MAGENTA}[#]{Fore.WHITE} {msg}")
    except Exception as e:
        print(f"Erro ao imprimir mensagem de hack: {e}")

def print_item(msg):
    try:
        print(f" ├─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir item: {e}")

def print_item_c(msg):
    try:
        print(f" │   ├─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir item com indentação: {e}")

def print_item_c_esc(msg):
    try:
        print(f" │      ├─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir item com indentação e escape: {e}")

def print_port(port, service):
    try:
        print(f" └─ {port}/tcp ({service})")
    except Exception as e:
        print(f"Erro ao imprimir porta: {e}")

def print_end_item(msg):
    try:
        print(f" └─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir item final: {e}")

def print_sub_item(msg):
    try:
        print(f" │   └─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir sub-item: {e}")

def print_sub_item_esc(msg):
    try:
        print(f" │      └─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir sub-item com escape: {e}")

def print_item_esc(msg):
    try:
        print(f"        ├─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir item com escape: {e}")

def print_end_item_esc(msg):
    try:
        print(f"        └─ {msg}")
    except Exception as e:
        print(f"Erro ao imprimir item final com escape: {e}")