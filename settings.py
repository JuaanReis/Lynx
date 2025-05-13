# settings.py

# Configurações de modo
DEBUG = True
OPERATION_MODE = "test"

# Configurações dos scanners
XSS_TIMEOUT = 10
PATH_SCAN_DEPTH = 3
PATH_TIMEOUT = 15
BRUTE_FORCE_MAX_RETRIES = 5
BRUTE_FORCE_TIMEOUT = 10

# Configurações de banco de dados ou API
DATABASE_URI = "mysql://user:password@localhost/lynx_database"
API_ENDPOINT = "https://api.lynxsec.io"
API_KEY = "sua_chave_api_aqui"

# Configurações de log
LOGGING_ENABLED = True
LOG_FILE_PATH = "logs/lynx_tool.log"
LOG_LEVEL = "DEBUG"

# Mensagem de alerta
LEGAL_USE_ONLY = False
ALERT_MESSAGE = """
[ALERTA] Esta ferramenta é destinada exclusivamente para testes de segurança em ambientes controlados e com permissão explícita. O uso indevido pode resultar em consequências legais. O autor não se responsabiliza por qualquer uso ilegal.
"""

# Outras configurações globais
VERBOSE_OUTPUT = True
USER_AGENT = "LYNX Web Security Scanner v1.0"
