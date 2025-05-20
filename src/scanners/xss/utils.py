from urllib.parse import urlunparse
import re
from colorama import Fore, init
import requests
import copy
from urllib.parse import urlencode
from src.utils.config import load_header

init(autoreset=True)

HEADERS = load_header()

def build_url(parsed_url, new_query):
    scheme = parsed_url.scheme if "localhost" not in parsed_url.netloc else ""
    netloc = "" if "localhost" in parsed_url.netloc else parsed_url.netloc
    path = parsed_url.path
    return urlunparse((scheme, netloc, path, parsed_url.params, new_query, parsed_url.fragment)).lstrip("/")

def payload_exe(payload, html):
    dangerous_contexts = [
        r'<script[^>]*>.*?' + re.escape(payload) + r'.*?</script>',
        r'on\w+\s*=\s*["\'].*?' + re.escape(payload) + r'.*?["\']',
        r'src\s*=\s*["\'].*?' + re.escape(payload) + r'.*?["\']',
        r'javascript:\s*' + re.escape(payload),
        re.escape(payload)
    ]
    for pattern in dangerous_contexts:
        if re.search(pattern, html, re.IGNORECASE | re.DOTALL):
            return True
    return False

def extrair_campos_formulario(form):
    campos = {}
    for inp in form.find_all("input"):
        tipo = inp.get("type", "text").lower()
        nome = inp.get("name")
        if nome and tipo in ["text", "search", "hidden", "email", "url"]:
            campos[nome] = ""
    for txt in form.find_all("textarea"):
        nome = txt.get("name")
        if nome:
            campos[nome] = ""
    return campos

def exibir_resultados(resultados):
    print(f"{Fore.YELLOW}[!] " + f"{Fore.WHITE} Resultados do Scanner")
    if resultados:
        for i, (payload, url) in enumerate(resultados):
            print(f"{Fore.GREEN}[+]" + f"{Fore.WHITE} XSS detectado: Refletido: {payload} --> {url}")
    else:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Nenhum XSS detectado.")


def testar_payload(payload, key, parsed_url, params):
    try:
        test_param = copy.deepcopy(params)
        test_param[key] = [payload]
        new_query = urlencode(test_param, doseq=True)
        full_url = build_url(parsed_url, new_query)
        response = requests.get(full_url, headers=HEADERS, timeout=10)
        if payload in response.text and payload_exe(payload, response.text):
            return (payload, full_url)
    except Exception as e:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Requisição falhou: {e}")
    return None

def testar_payload_stored(payload, campos, post_url, view_url):
    try:
        data = campos.copy()
        for k in data:
            data[k] = payload

        requests.post(post_url, data=data, timeout=10, headers=HEADERS)
        view = requests.get(view_url, timeout=10)

        if payload in view.text:
            return (payload, True)
        else:
            return (payload, False)
    except Exception as e:
        return (payload, f"Erro: {e}")