from urllib.parse import urljoin
import requests
from colorama import Fore, init
from threading import Lock
import time
from src.utils.config import load_header
from .response import is_valid_response
from src.utils.file_logs import setup_logs

init(autoreset=True)

setup_logs()
lock = Lock()
found_path = []

HEADERS = load_header()

def check_path(path, base_url, valid_status, delay_range, mode, fake_body):
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=False)
        if is_valid_response(response, valid_status):
            # Compara o corpo da resposta com o corpo fake
            if fake_body is None or response.text.strip() != fake_body.strip():
                with lock:
                    found_path.append((url, response.status_code))
        elif response.status_code == 429:
            time.sleep(5)
            return check_path(path, base_url, valid_status, delay_range, mode, fake_body)
    except Exception as e:
        print(f"{Fore.RED}[ERRO]:{Fore.WHITE}{e}")