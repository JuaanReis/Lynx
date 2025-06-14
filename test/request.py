import requests
from bs4 import BeautifulSoup as bs
import time
import ipaddress
import socket
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

PROXY = {
  "http": "socks5h://127.0.0.1:9050",
  "https": "socks5h://127.0.0.1:9050"
}

def verify_proxy():
  test_url = "http://httpbin.org/ip"
  try:
    response = requests.get(test_url, proxies=PROXY, timeout=5)
    if response.status_code == 200:
        print("Proxy configurado e funcionando.")
    else:
        print("Proxy configurado, mas não respondeu corretamente.")
        sys.exit(0)
  except Exception as e:
    print(f"Erro ao verificar o proxy: {e}")
    sys.exit(1)

def req(timeout=10):
  """Teste de requisição HTTP."""
  try:
    url = input("Digite a URL ou um IP para teste: ")
    # Extrai apenas o host (caso o usuário coloque http://)
    host = url.split('/')[0] if '://' not in url else url.split('/')[2]
    try:
      ipaddress.ip_address(host)
      print("Você digitou um IP.")
    except ValueError:
      print("Você digitou um domínio.")
    if not url.startswith(('http://', 'https://')):
      url = 'http://' + url
    print(f"Header enviado: {HEADERS}")
    print(f"Proxy utilizado: {PROXY}\n")
    start = time.time()
    ip = socket.gethostbyname(host)
    print(f"Ip: {ip}")
    response = requests.get(url, timeout=timeout, headers=HEADERS, proxies=PROXY)
    end = time.time()
    print(f"Requisição feita em {end - start:.2f} segundos.\n")
    return response
  except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer requisição para {url}: {e}")
    return None

if __name__ == "__main__":
  try:
    verify_proxy()
    response = req()
    if response:
      print(f"Status Code: {response.status_code}\n")
      print(f"Headers: {response.headers}\n")
      soup = bs(response.text, 'html.parser')
      title = soup.title.string if soup.title else "No title found"
      print(f"Title: {title}\n")
      date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      print(f"Data e hora da requisição: {date}\n")
      data_server = response.headers.get("Date", "Não informado pelo servidor")
      print(f"Data e hora do servidor: {data_server}\n")
    else:
      print("Requisição falhou.")
  except KeyboardInterrupt:
    print("\nOperação cancelada pelo usuário.")
    sys.exit(0)
  except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
    sys.exit(1)
