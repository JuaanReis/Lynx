import time
import socket

def test_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Testa a conexão com um host e porta específicos.
    Retorna True se a conexão for bem-sucedida, caso contrário, retorna False.
    """
    try:
        inicio = time.time()
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        fim = time.time()
        s.close()
        return True, round((fim - inicio) * 1000, 2)  # Retorna o tempo em milissegundos
    except Exception as e:
        return False, str(e)