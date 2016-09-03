import logging
from logging.handlers import RotatingFileHandler

def getLoggerHandler(logFileName):
    handler = RotatingFileHandler(logFileName, maxBytes=100000000, backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    return handler

def getLogger(loggerName):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    logFileName = "logs/reader.log"
    handler = getLoggerHandler(logFileName)
    logger.addHandler(handler)
    return logger
