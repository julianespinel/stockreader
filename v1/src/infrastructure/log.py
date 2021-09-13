import os
import logging
from logging.handlers import RotatingFileHandler

def get_logger_handler(logFileName):
    handler = RotatingFileHandler(logFileName, maxBytes=100000000, backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    return handler

def get_logger(loggerName):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    directory = "logs"
    file_name = "stockreader.log"
    os.makedirs(directory, exist_ok=True)
    handler = get_logger_handler(directory + "/" + file_name)
    logger.addHandler(handler)
    return logger
