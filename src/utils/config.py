"""Carrega as configurações do arquivo JSON e retorna um dicionário com as informações necessárias para a execução do programa."""

#Headers
def load_header(path="data/config.json"):
  import json
  with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data.get("headers", {})

#Host
def load_host(path="data/config.json"): 
  import json
  with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data.get("host", {})