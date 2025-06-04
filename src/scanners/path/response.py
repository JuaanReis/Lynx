from .title import get_title

def is_valid_response(response, valid_status):
    if response.status_code not in valid_status:
        return False
    content = response.text.lower()
    title = get_title(response.text)
    invalid_patterns = [
        "not found", "404", "não encontrado", "page not available",
        "error 404", "404 error", "página não encontrada", "file not found",
        "the page you requested could not be found", "does not exist",
        "no encontrado", "不存在", "nie znaleziono", "non trovato",
        "not exist", "not available", "not be found", "not exists",
        "not found on this server", "404 -", "404:", "404.", "404 ",
        "404 page", "404pagenotfound", "404 notfound", "404 not found",
        "documento não encontrado", "document not found", "page not found",
        "servidor não encontrado", "server not found", "pagina não encontrada", "invalid request:"
    ]
    return not any(p in content or p in title for p in invalid_patterns)