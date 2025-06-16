def extrair_campos_formulario(form):
    campos = {}
    for inp in form.find_all("input"):
        tipo = inp.get("type", "text").lower()
        nome = inp.get("name")
        if nome and tipo in ["text", "search", "hidden", "email", "url"]:
            campos[nome] = ""
    for txt in form.find_all("textarea"):
        nome = txt.get("name")
        if nome:
            campos[nome] = ""
    return campos