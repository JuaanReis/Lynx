import requests
from bs4 import BeautifulSoup

def get_forms(url):
    """Verificar quais formulários estão disponíveis na URL e retornar método, action e campos."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        all_forms = []
        for form in forms:
            form_info = {
                "action": form.get("action", ""),
                "method": form.get("method", "GET").upper(),
                "inputs": []
            }
            inputs = form.find_all("input")
            for input_tag in inputs:
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name", "")
                input_value = input_tag.get("value", "")
                form_info["inputs"].append({
                    "type": input_type,
                    "name": input_name,
                    "value": input_value
                })
            all_forms.append(form_info)
        return all_forms
    except Exception as e:
        return []