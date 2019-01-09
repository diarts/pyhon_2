import logging.handlers
from loggers import check_logger

time_rotating_logger = logging.handlers.TimedRotatingFileHandler(filename='logs/server/server_system_out.log',
                                                                 interval=1, when='M', backupCount=5,
                                                                 encoding='utf-8')
time_rotating_logger.setLevel(logging.DEBUG)
time_rotating_logger.setFormatter(check_logger.file_rotate_formatter)

server_logger = logging.getLogger('server_logger')
server_logger.addHandler(check_logger.console_logger)
server_logger.addHandler(time_rotating_logger)
server_logger.setLevel(logging.DEBUG)
