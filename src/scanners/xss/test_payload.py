import copy
from urllib.parse import urlencode
from .build_url import build_url
from .payload import payload_exe
import requests
from colorama import Fore, init
from src.utils.config import load_header
from src.utils.proxy import load_proxy


init(autoreset=True)

HEADERS = load_header()
PROXY = load_proxy()

def testar_payload(payload, key, parsed_url, params):
    try:
        test_param = copy.deepcopy(params)
        test_param[key] = [payload]
        new_query = urlencode(test_param, doseq=True)
        full_url = build_url(parsed_url, new_query)
        response = requests.get(full_url, headers=HEADERS, proxies=PROXY, timeout=10)
        if payload in response.text and payload_exe(payload, response.text):
            return (payload, full_url)
    except Exception as e:
        print(f"{Fore.RED}[-]" + f"{Fore.WHITE} Requisição falhou: {e}")
    return None