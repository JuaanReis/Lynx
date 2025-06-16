import requests
from src.utils.config import load_header
from src.utils.proxy import load_proxy

HEADERS = load_header()
PROXY = load_proxy()

def testar_payload_stored(payload, campos, post_url, view_url):
    try:
        data = campos.copy()
        for k in data:
            data[k] = payload

        requests.post(post_url, data=data, timeout=10, headers=HEADERS, proxies=PROXY)
        view = requests.get(view_url, timeout=10)

        if payload in view.text:
            return (payload, True)
        else:
            return (payload, False)
    except Exception as e:
        return (payload, f"Erro: {e}")