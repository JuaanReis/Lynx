import requests

def get_tecnologies(url):
  """Detecta a tecnologia por tras do site"""
  try:
    response = requests.get(url, timeout=10)
    headers = response.headers
    tecnologias = {}

    #Servidor web
    if "Server" in headers:
      tecnologias["Servidor"] = headers["Server"]

    #Backend comum
    backends = []
    if "X-Powered-By" in headers:
      backends.append(headers["X-Powered-By"])
    if "X-AspNet-Version" in headers:
      backends.append("ASP.NET " + headers["X-AspNet-Version"])
    if backends:
      tecnologias["Backend"] = backends

    #CDN comum
    cdn_headers = [
      ("Cloudflare", "CF-RAY"),
      ("Akamai", "X-Akamai-Transformed"),
      ("Sucuri", "X-Sucuri-ID"),
      ("Fastly", "Fastly-SSL"),
      ("Amazon CloudFront", "X-Amz-Cf-Id"),
      ("StackPath", "X-CDN"),
      ("Incapsula", "X-CDN"),
      ("Google", "X-Goog-Hash"),
    ]
    cdns = []
    for nome, cab in cdn_headers:
      if cab in headers:
        cdns.append(nome)
    if cdns:
      tecnologias["CDN"] = cdns

    #APIs detectadas
    apis = []
    for k, v in headers.items():
      if "api" in k.lower() or "api" in v.lower():
        apis.append(f"{k}: {v}")
    if apis:
      tecnologias["APIs"] = apis

    return tecnologias if tecnologias else {"Info": "Nenhuma tecnologia detectada"}
  except Exception as e:
    return {"Erro": str(e)}