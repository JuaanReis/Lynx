import logging

def logs(args, domain):
  try:
    """Registra logs de execução do scanner de XSS"""
    logging.info(f"Executando o scanner de XSS com os seguintes parâmetros: {args}")
    logging.info(f"Payloads carregados: {args.payload}")
    logging.info(f"Tipo de ataque: {args.type}")
    logging.info(f"URL alvo: {args.url}")
    logging.info(f"Limite de payloads: {args.limit}")
    logging.info(f"Threads: {args.thread}")

    logging.info(f"URL testada: {args.url}")
    logging.error(f"Host {domain} esta bloqueado por motivos de segurança.")
  except Exception as e:
    logging.error(f"Erro ao registrar logs: {e}")
    print(f"[ERRO] Algo deu ruim ao registrar logs: {e}")