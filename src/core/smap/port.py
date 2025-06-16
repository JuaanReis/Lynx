import socket
from concurrent.futures import ThreadPoolExecutor

def scan_ports(host, ports, timeout=10):
    """Lê as portas de um host e retorna uma lista de portas abertas."""
    def check_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                if result == 0:
                    return port
                else:
                    return None
        except Exception:
            pass
        return None

    open_ports = []
    try:
        with ThreadPoolExecutor(max_workers=300) as executor:
            results = executor.map(check_port, ports)
            open_ports = [port for port in results if port is not None]
        return open_ports
    except Exception as e:
        print(f"Erro ao escanear portas: {e}")
        return []