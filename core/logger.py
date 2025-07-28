import logging
import logging.handlers
import os
import sys

LOG_DIR = 'logs'
LOG_FILE = 'form_filler.log'

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("AutoFormFiller")
logger.setLevel(logging.INFO)

fromatter = logging.Formatter("%(asctime)s - %(name)s - %(levelame)s - %(message)s")

file_handler = logging.handlers.RotatingFileHandler(os.path.join(LOG_DIR,LOG_FILE), maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(fromatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(fromatter)

if not logger.hasHandlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)