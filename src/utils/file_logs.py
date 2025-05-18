import os
import logging
from datetime import datetime

#Criar logs
def setup_logs():
  """Cria um arquivo de log para registrar as atividades do scanner."""
  log_dir = "./output/logs"
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)

  log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_scan_logs.txt"
  log_path = os.path.join(log_dir, log_filename)

  logging.basicConfig(
      filename=log_path,
      filemode="w",
      level=logging.INFO,
      format="%(asctime)s - %(levelname)s - %(message)s",)