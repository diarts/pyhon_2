import logging.handlers

console_formatter = logging.Formatter('%(name)-15s %(levelname)-7s %(asctime)s %(funcName)-5s | %(message)s')
console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)
console_logger.setFormatter(console_formatter)

file_logger_formatter = logging.Formatter(
    '%(name)-15s %(levelname)-7s %(asctime)s %(module)s %(funcName)-5s line:%(lineno)d | %(message)s')
file_rotating_logger = logging.handlers.RotatingFileHandler(filename='logs/client/client_system_out.log',
                                                            maxBytes=10000, backupCount=5, encoding='utf-8')
file_rotating_logger.setLevel(logging.DEBUG)
file_rotating_logger.setFormatter(file_logger_formatter)

file_time_rotating_logger = logging.handlers.TimedRotatingFileHandler(filename='logs/server/server_system_out.log',
                                                                      interval=1, when='M', backupCount=5, utc='UTC',
                                                                      encoding='utf-8')
file_time_rotating_logger.setLevel(logging.DEBUG)
file_time_rotating_logger.setFormatter(file_logger_formatter)

ip_and_port_checker_logger = logging.getLogger('ip&port_checker_logger')
ip_and_port_checker_logger.addHandler(console_logger)
ip_and_port_checker_logger.setLevel(logging.DEBUG)

client_logger = logging.getLogger('client_logger')
client_logger.addHandler(console_logger)
client_logger.addHandler(file_rotating_logger)
client_logger.setLevel(logging.DEBUG)

server_logger = logging.getLogger('server_logger')
server_logger.addHandler(console_logger)
server_logger.addHandler(file_time_rotating_logger)
server_logger.setLevel(logging.DEBUG)
