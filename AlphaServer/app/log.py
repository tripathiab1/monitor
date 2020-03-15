# -*- coding: utf-8 -*-

import os

import logging
from logging.handlers import RotatingFileHandler
from glog import GlogFormatter

LOG_FILE = "logs/monitor.log"

BACKUP_COUNT = 5
MAX_BYTES = 10<<20
MODE = 'a'

def log_setup(comp_logger, log_level):
    """
       This function will configure and return logger
       object for respective component.
    """
    logger = logging.getLogger(comp_logger)
    file_handler = RotatingFileHandler(filename=LOG_FILE, mode=MODE,
                                       maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(GlogFormatter())
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.propagate = 0
    return logger
