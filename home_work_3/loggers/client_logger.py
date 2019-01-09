import logging.handlers
from loggers import check_logger

file_rotating_logger = logging.handlers.RotatingFileHandler(filename='logs/client/client_system_out.log',
                                                            maxBytes=10000, backupCount=5, encoding='utf-8')
file_rotating_logger.setLevel(logging.DEBUG)
file_rotating_logger.setFormatter(check_logger.file_rotate_formatter)

client_logger = logging.getLogger('client_logger')
client_logger.addHandler(check_logger.console_logger)
client_logger.addHandler(file_rotating_logger)
client_logger.setLevel(logging.DEBUG)
