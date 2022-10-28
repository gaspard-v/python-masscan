import logging
import logging.handlers
import logging.config
import os

logging.config.fileConfig('logging.ini')

# create logger
logger = logging.getLogger(__name__)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
try:
    os.remove("ifhjifuejfuiehfueheu_ihfej")
except Exception as err:
    logger.warning(err)
print("OK")
