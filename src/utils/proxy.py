"""Função que carrega as configurações de proxy do arquivo JSON e retorna um dicionário com as informações necessárias para a execução do programa."""

def load_proxy(path="data/config.json"):
  import json
  with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data.get("proxy", {})