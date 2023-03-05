import logging
from logging.handlers import RotatingFileHandler
import os

LogBasePath = "/var/vkr/log/"

if not os.path.exists(LogBasePath):
   os.makedirs(LogBasePath)

LogDebugPath = LogBasePath + 'vkr.debug.log'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatterDebug = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s',datefmt=' %d/%m/%Y %H:%M:%S')
handlerDebug = RotatingFileHandler(LogDebugPath, mode='a')
handlerDebug.setLevel(logging.DEBUG)
handlerDebug.setFormatter(formatterDebug)
logger.addHandler(handlerDebug)
logger.info("Logger debug created")