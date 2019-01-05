class IpAndPortChecker:
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
        if not my_function:
            self._help_function = self._default_help_function
        elif hasattr(my_function, '__call__'):
            self._help_function = my_function
        else:
            raise ValueError('В параметр help function была передана не функция')

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
            raise ValueError('eject_type был указан не верно')

    # has unittest
    def check_ip_counts(self, count: int):
        if type(count) == int and count <= self._MAX_VALUE_IP:
            return True
        else:
            raise self._my_value_error_ip

    # has unittest
    def ip_split(self, ip: str, splitter: str):
        try:
            return ip.split(splitter)
        except AttributeError:
            raise self._my_value_error_ip

    # has unittest
    def ip_list_items_convert_to_int(self, ip):
        for index, item in enumerate(ip):
            try:
                new_item = int(item)
            except ValueError:
                raise self._my_value_error_ip
            else:
                self.check_ip_counts(new_item)
                ip[index] = new_item
        return ip

    # has unittest
    def check_ip(self, ip: str):
        ip = self.ip_split(ip=ip, splitter='.')
        ip = self.ip_list_items_convert_to_int(ip)
        return ip

    # has_unittest
    def check_port(self, port):
        try:
            port = int(port)
        except ValueError:
            raise self._my_value_error_port

        if self._MIN_PORT <= port <= self._MAX_PORT:
            return port
        else:
            raise self._my_value_error_port

    # has unittest
    def get_index_sys_arg(self, key, my_system_args):
        try:
            index = my_system_args.index(key)
        except ValueError:
            return False
        else:
            return index

    # has unittest
    def get_variable(self, my_system_args, index):
        try:
            new_var = my_system_args[index + 1]
        except IndexError:
            raise self._my_value_error_variable
        else:
            return new_var

    def check_new_var(self, key, new_var):
        if key == '-a':
            self.check_ip(new_var)
        elif key == '-p':
            self.check_port(new_var)
        return new_var

    # has unittest
    def add_variables(self, my_system_args, my_variables):
        for key in my_variables.keys():
            if key in my_system_args:
                index = self.get_index_sys_arg(key, my_system_args)
                if not index:
                    continue

                new_var = self.get_variable(my_system_args, index)
                my_variables[key] = self.check_new_var(key, new_var)
        return my_variables

    def check_sys_args(self, my_system_args, my_variables):
        """check is input a right and set ip and host parameters
        -a  - is ip string
        -p  - is port number
        -un - is user name (for client)"""

        if len(my_system_args) == 2 and my_system_args[1] == 'help':
            self._help_function()
            return False

        elif len(my_system_args) == 1:
            return my_variables

        else:
            my_variables = self.add_variables(my_system_args, my_variables)
        return my_variables


if __name__ == '__main__':
    import sys

    sys_args = sys.argv

    checker = IpAndPortChecker()
    my_variables = checker.check_sys_args(sys_args, {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckina'})
    if not my_variables:
        exit(0)
    else:
        print(my_variables)