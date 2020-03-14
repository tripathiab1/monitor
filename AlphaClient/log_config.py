
import os

import logging
from logging.handlers import RotatingFileHandler
from glog import GlogFormatter

MAIN_THREAD_LOG_FILE = "logs/monitor.logs"

BACKUP_COUNT = 5
MAX_BYTES = 10<<20
MODE = 'a'

def log_setup(comp_logger, log_file, log_level):
    """
       This function will configure and return logger
       object for respective component.
    """
    logger = logging.getLogger(comp_logger)
    file_handler = RotatingFileHandler(filename=log_file, mode=MODE,
                                       maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(GlogFormatter())
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    return logger

