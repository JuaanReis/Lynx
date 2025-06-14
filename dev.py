from colorama import Fore, init
import shlex
from argparse import ArgumentParser

init(autoreset=True)

def parse_args():
  parser = ArgumentParser(description="Ferramentas de desenvolvedor")
  parser.add_argument("--xss", action="store_true", help="Ativar modo de depuração")
  parser.add_argument("--path", action="store_true", help="Ativar modo de depuração")
  parser.add_argument("--smap", action="store_true", help="Ativar modo de depuração")
  args = parser.parse_args()
  return args

def main(args):
  """Executa o scanner de acordo com o modo especificado"""
  if args.xss:
      from src.scanners import xss
      user_input = input(f"{Fore.GREEN}>   {Fore.WHITE}")
      user_args = shlex.split(user_input)
      try:
        xss.run(user_args)
      except Exception as e:
        print(f"{Fore.RED}[!]{Fore.WHITE}{e}")
  elif args.path:
      from src.scanners import path
      user_input = input(f"{Fore.GREEN}>   {Fore.WHITE}")
      user_args = shlex.split(user_input)
      try:
        path.run(user_args)
      except Exception as e:
        print(f"{Fore.RED}[!]{Fore.WHITE}{e}")
  elif args.smap:
      from src.scanners import smap
      user_input = input(f"{Fore.GREEN}>   {Fore.WHITE}")
      user_args = shlex.split(user_input)
      try:
        smap.run(user_args)
      except Exception as e:
        print(f"{Fore.RED}[!]{Fore.WHITE}{e}")
  else:
      print(f"{Fore.RED}[!] Modo não especificado.")

if __name__ == "__main__":
  try:
      args = parse_args()
      main(args)
  except KeyboardInterrupt:
      print(f"{Fore.RED}[!]{Fore.WHITE} Interrompido pelo usuário.")
  except Exception as e:
      print(f"{Fore.RED}[!]{Fore.WHITE} Erro inesperado: {e}")
