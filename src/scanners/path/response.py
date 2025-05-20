def is_valid_response(response, valid_status):
    if response.status_code not in valid_status:
        return False
    content = response.text.lower()
    invalid_patterns = ["not found", "404", "não encontrado", "page not available"]
    return not any(p in content for p in invalid_patterns)