import requests
from colorama import Fore, init

init(autoreset=True)
def get_cookies(url):
  try:
    response = requests.get(url, timeout=10)
    cookies = response.cookies
    if not cookies:
      return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum cookie encontrado."]
    detalhes = []
    for cookie in cookies:
      info = f"{cookie.name}={cookie.value}"
      info += f" | Domain: {cookie.domain}"
      info += f" | Path: {cookie.path}"
      info += f" | Secure: {cookie.secure}"
      info += f" | HttpOnly: {getattr(cookie, 'httponly', False)}"
      info += f" | SameSite: {getattr(cookie, 'samesite', 'Não informado')}"
      info += f" | Expires: {cookie.expires if cookie.expires else 'Não informado'}"
      detalhes.append(info)
    return detalhes
  except Exception as e:
    return [f"{Fore.RED}[-]" + f"{Fore.WHITE} Erro ao coletar cookies: {e}"]