import logging

console_formatter = logging.Formatter('%(name)-15s %(levelname)-7s %(asctime)s %(funcName)-5s | %(message)s')
file_rotate_formatter = logging.Formatter(
    '%(name)-15s %(levelname)-7s %(asctime)s %(module)s %(funcName)-5s line:%(lineno)d | %(message)s')

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)
console_logger.setFormatter(console_formatter)

ip_and_port_checker_logger = logging.getLogger('ip&port_checker_logger')
ip_and_port_checker_logger.addHandler(console_logger)
ip_and_port_checker_logger.setLevel(logging.DEBUG)
