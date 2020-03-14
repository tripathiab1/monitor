# -*- coding: utf-8 -*-

import os
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)
LOG_LEVEL = CONFIG['logging']['level']

