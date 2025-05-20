import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime

def get_ssl(url):
  """Verificar o certificado SSL do site"""
  hostname = urlparse(url).hostname
  context = ssl.create_default_context()
  try:
    with socket.create_connection((hostname, 443), timeout=10) as sock:
      with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        cert = ssock.getpeercert()
        espira = datetime.strptime(cert.get('notAfter'), '%b %d %H:%M:%S %Y %Z')
        status = "valido" if espira > datetime.now() else "expirado"
        return {
          "status": status,
          "validade": espira.strftime('%Y-%m-%d %H:%M:%S'),
          "issuer": dict(x[0] for x in cert['issuer']),
          "subject": dict(x[0] for x in cert['subject']),
          "serialNumber": cert['serialNumber'],
          "version": cert['version'],
          "notBefore": cert['notBefore'],
          "notAfter": cert['notAfter']
        }
  except Exception as e:
    return {"status": "erro", "message": str(e)}