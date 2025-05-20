def load_proxy(path="data/config.json"):
  import json
  with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data.get("proxy", {})