import re

"""Pega o titulo de uma página web"""
def get_title(content):
  match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
  if match:
    return match.group(1).strip().lower()
  return "" 