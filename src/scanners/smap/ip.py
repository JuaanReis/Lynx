import socket

def get_ipv4(host, timeout=5):
  """Pega o IP pelo host"""
  try:
    socket.setdefaulttimeout(timeout)
    ip = socket.gethostbyname(host)
    return ip
  except socket.gaierror:
    return f"IP de {host} não encontrado"
  except Exception as e:
    print(f"Erro ao obter IP: {e}")
    return None

def get_ipv6(host, timeout=5):
    """Pega o IPv6 pelo host"""
    try:
        socket.setdefaulttimeout(timeout)
        ipv6 = socket.getaddrinfo(host, None, socket.AF_INET6)
        if ipv6:
          return [addr[4][0] for addr in ipv6]
        else:
          return f"IPv6 de {host} não encontrado"
    except socket.gaierror:
        return f"IPv6 de {host} não configurado"
    except Exception as e:
        print(f"Erro ao obter IPv6: {e}")
        return None