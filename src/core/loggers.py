import logging
import os
from logging.handlers import RotatingFileHandler

logs_folder = 'logs'
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

logger_file = logging.getLogger('file_logger')
logger_file.setLevel(logging.INFO)
file_handler = RotatingFileHandler(
    os.path.join(logs_folder, 'power_supply.log'),
    maxBytes=20 * 1024 * 1024,
    backupCount=5
)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger_file.addHandler(file_handler)

logger_console = logging.getLogger('console_logger')
logger_console.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger_console.addHandler(console_handler)
