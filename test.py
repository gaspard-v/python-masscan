import logging, logging.handlers, logging.config

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
    raise Exception("OOOF")
except Exception as err:
    logger.exception(err)
print("OK")