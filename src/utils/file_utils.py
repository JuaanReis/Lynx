import os

def load_payloads(filename, max_lines=None):
    path = os.path.join("payloads", filename)
    payloads = []

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if max_lines is not None and i >= max_lines:
                break
            stripped = line.strip()
            if stripped:
                payloads.append(stripped)

    return payloads
