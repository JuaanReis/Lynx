import re

def payload_exe(payload, html):
    dangerous_contexts = [
        r'<script[^>]*>.*?' + re.escape(payload) + r'.*?</script>',
        r'on\w+\s*=\s*["\'].*?' + re.escape(payload) + r'.*?["\']',
        r'src\s*=\s*["\'].*?' + re.escape(payload) + r'.*?["\']',
        r'javascript:\s*' + re.escape(payload),
        re.escape(payload)
    ]
    for pattern in dangerous_contexts:
        if re.search(pattern, html, re.IGNORECASE | re.DOTALL):
            return True
    return False