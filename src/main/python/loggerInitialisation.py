import logging

loggingFormat = '%(asctime)-15s %(message)s'
logging.basicConfig(format=loggingFormat)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

