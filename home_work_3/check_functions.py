import logging, loggers

ip_and_port_checker_logger = logging.getLogger('ip&port_checker_logger')


class IpAndPortChecker:
    _MIN_VALUE_IP = 0
    _MAX_VALUE_IP = 255
    _MIN_PORT = 1025
    _MAX_PORT = 65535
    _WRONG_VARIABLE_MESS = 'Вы неправильно указали переменные для запуска, если вам требуется помощь для запуска' \
                           'программы воспользуйтесь параметром -help'
    _WRONG_IP_MESS = 'Указан неверный IP адресс, IP адресс должен иметь вид X.X.X.X, где каждый X это число от 0 - 255'
    _WRONG_PORT_MESS = 'Порт для подключения должен быть числом в диапазоно 1025 - 65535'

    def __init__(self, help_function=None):
        self._init_help_function(help_function)
        self._my_value_error_ip = ValueError(self.ejection_program(eject_type='ip'))
        self._my_value_error_port = ValueError(self.ejection_program(eject_type='port'))
        self._my_value_error_variable = ValueError(self.ejection_program(eject_type='variable'))

    # has unittest
    def _init_help_function(self, my_function):
        ip_and_port_checker_logger.debug('check whether transfer var is a function or a method')
        if not my_function:
            ip_and_port_checker_logger.debug('as any variables were not transfer, help function set default')
            self._help_function = self._default_help_function
        elif hasattr(my_function, '__call__'):
            ip_and_port_checker_logger.debug('transfer var is a function or a method, it set as a help function')
            self._help_function = my_function
        else:
            ip_and_port_checker_logger.critical('transfer var is not a function, Exception Value error is raised')
            raise ValueError

    def _default_help_function(self):
        print('help')

    # has unittest
    def ejection_program(self, eject_type):
        if eject_type == 'ip':
            return self._WRONG_IP_MESS
        elif eject_type == 'port':
            return self._WRONG_PORT_MESS
        elif eject_type == 'variable':
            return self._WRONG_VARIABLE_MESS
        else:
            raise ValueError('wrong eject_type')

    # has unittest
    def check_ip_counts(self, count: int):
        ip_and_port_checker_logger.debug(f'check item: {count} in range '
                                         f'from {self._MIN_VALUE_IP} to {self._MAX_VALUE_IP}')
        if type(count) == int and self._MIN_VALUE_IP <= count <= self._MAX_VALUE_IP:
            ip_and_port_checker_logger.debug(f'check success, item: {count} is in required range')
            return True
        else:
            ip_and_port_checker_logger.critical(f'{count} not in range from {self._MIN_VALUE_IP} to '
                                                f'{self._MAX_VALUE_IP}, Exception Value error is raised')
            raise self._my_value_error_ip

    # has unittest
    def ip_split(self, ip: str, splitter: str):
        try:
            return ip.split(splitter)
        except AttributeError:
            ip_and_port_checker_logger.critical(f'split variable {ip} is failed, Exception Value error is raised')
            raise self._my_value_error_ip

    # has unittest
    def ip_list_items_convert_to_int(self, ip):
        for index, item in enumerate(ip):
            ip_and_port_checker_logger.debug(f'converting item: {item} to integer')
            try:
                new_item = int(item)
            except ValueError:
                ip_and_port_checker_logger.critical(f'converting item: {item} to integer is failed, '
                                                    'Exception Value error be raised')
                raise self._my_value_error_ip
            else:
                ip_and_port_checker_logger.debug(f'converting is successful')
                self.check_ip_counts(new_item)
                ip[index] = new_item
                ip_and_port_checker_logger.debug('value meets requirement, next item')
        return ip

    # has unittest
    def check_ip(self, ip: str):
        ip_and_port_checker_logger.debug('run split string variable by .')
        ip = self.ip_split(ip=ip, splitter='.')

        ip_and_port_checker_logger.debug('split is successful, run convert item of ip list to integer')
        ip = self.ip_list_items_convert_to_int(ip)
        ip_and_port_checker_logger.debug(f'converting is successful, ip address: {ip} meets required')
        return ip

    # has_unittest
    def check_port(self, port):
        ip_and_port_checker_logger.debug(f'check port: {port} is integer')
        try:
            port = int(port)
        except ValueError:
            ip_and_port_checker_logger.critical(f'converting port: {port} to integer is failed, '
                                                'Exception Value error is raised')
            raise self._my_value_error_port

        ip_and_port_checker_logger.debug('success, check whether port is in range '
                                         f'from {self._MIN_PORT} to {self._MAX_PORT}')
        if self._MIN_PORT <= port <= self._MAX_PORT:
            ip_and_port_checker_logger.debug('port meets required')
            return port
        else:
            ip_and_port_checker_logger.critical(
                f'port: {port} is not in range from {self._MIN_PORT} to {self._MAX_PORT}, '
                'Exception Value error is raised')
            raise self._my_value_error_port

    # has unittest
    def get_variable(self, my_system_args, index):
        try:
            new_var = my_system_args[index + 1]
        except IndexError:
            ip_and_port_checker_logger.critical(f'getting argument is failed, system arguments list: {my_system_args} '
                                                'has not this argument. Exception Value error is raised')
            raise self._my_value_error_variable
        else:
            ip_and_port_checker_logger.debug(f'getting new argument {new_var} is successful')
            return new_var

    def check_new_var(self, key, new_var):
        if key == '-a':
            ip_and_port_checker_logger.debug(f'run check {new_var} meets required ip address')
            self.check_ip(new_var)
        elif key == '-p':
            ip_and_port_checker_logger.debug(f'run check {new_var} meets required port')
            self.check_port(new_var)
        return new_var

    # has unittest
    def add_variables(self, my_system_args, my_variables):
        ip_and_port_checker_logger.debug('start add variables')

        for key in my_variables.keys():

            ip_and_port_checker_logger.debug(f'get key: {key}, from my variables and find it in sys args list')
            if key in my_system_args:
                ip_and_port_checker_logger.debug(f'get index of key: {key} in sys args list ')
                index = my_system_args.index(key)

                ip_and_port_checker_logger.debug(f'try to get variable by index = {index}')
                new_var = self.get_variable(my_system_args, index)

                ip_and_port_checker_logger.debug(f'run check of variable: {new_var} meets required type')
                my_variables[key] = self.check_new_var(key, new_var)
                ip_and_port_checker_logger.debug(f'default value has been replaced to new: {new_var}')
            else:
                ip_and_port_checker_logger.debug(f'system args list has not key: {key}, take next key')

        ip_and_port_checker_logger.debug(f'add variables is finished, return new variables list: {my_variables}')
        return my_variables

    def check_sys_args(self, my_system_args, my_variables):
        """check is input a right and set ip and host parameters
        -a:     is ip string
        -p:     is port number
        -un:    is user name (for client)"""

        ip_and_port_checker_logger.debug('check system arguments starting')
        if len(my_system_args) == 2 and my_system_args[1] == 'help':
            ip_and_port_checker_logger.debug('function starts with help argument, start help function')
            self._help_function()
            ip_and_port_checker_logger.debug('help function is over, close check system arguments function')
            return False

        elif len(my_system_args) == 1:
            ip_and_port_checker_logger.debug('program is not running through the console, '
                                             f'return of default startup parameters {my_variables}')
            return my_variables

        else:
            ip_and_port_checker_logger.debug('program is running through the console, run add_variables function '
                                             f'with next transfered system parameters {my_system_args}')
            my_variables = self.add_variables(my_system_args, my_variables)
            ip_and_port_checker_logger.debug(f'close check function and return startup parameters {my_variables}')
        return my_variables


if __name__ == '__main__':
    import sys

    ip_and_port_checker_logger.debug('getting system arguments')
    sys_args = sys.argv
    ip_and_port_checker_logger.debug('create ip and port checker')
    checker = IpAndPortChecker()
    my_variables = checker.check_sys_args(sys_args, {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckina'})

    if not my_variables:
        ip_and_port_checker_logger.debug('startup parameters dict is empty, exit from program')
        exit(0)
    else:
        print(my_variables)
