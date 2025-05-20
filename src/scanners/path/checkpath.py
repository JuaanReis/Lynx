from urllib.parse import urljoin
import requests
from colorama import Fore, init
from threading import Lock
import time
from src.utils.config import load_header
from src.utils.proxy import load_proxy
from .color import print_color
from .response import is_valid_response
from src.utils.file_logs import setup_logs

init(autoreset=True)

setup_logs()
lock = Lock()
found_path = []

HEADERS = load_header()
PROXY = load_proxy()

def check_path(path, base_url, valid_status, delay_range, mode):
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        response = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10, allow_redirects=False)

        if mode == "debug":
            print_color(f"{Fore.CYAN}DEBUG", f"Requisitando: {url} - Status: {response.status_code}")

        if is_valid_response(response, valid_status):
            with lock:
                found_path.append((url, response.status_code))
        elif response.status_code == 429:
            time.sleep(5)
            return check_path(path, base_url, valid_status, delay_range, mode)
    except Exception as e:
        pass