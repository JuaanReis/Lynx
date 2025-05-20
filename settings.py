# settings.py

# Configurações de modo
DEBUG = True
OPERATION_MODE = "test"

# Configurações de log
LOGGING_ENABLED = True
LOG_FILE_PATH = "output/"
LOG_LEVEL = "DEBUG"

# Mensagem de alerta
LEGAL_USE_ONLY = True
ALERT_MESSAGE = """
[ALERTA] Esta ferramenta é destinada exclusivamente para testes de segurança em ambientes controlados e com permissão explícita. O uso indevido pode resultar em consequências legais. O autor não se responsabiliza por qualquer uso ilegal.
"""
#Dev mode
DEV_MODE = True
DEV_MODE_MESSAGE = """
[!] Modo de desenvolvimento ativado. Algumas funcionalidades podem não estar disponíveis ou podem conter bugs.
[!] Use com cautela e apenas em ambientes controlados.
"""