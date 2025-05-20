from colorama import Fore, Style, init

init(autoreset=True)

def print_color(label, msg, cor=Fore.WHITE):
    print(f"{cor}[{label}]{Style.RESET_ALL} {msg}")