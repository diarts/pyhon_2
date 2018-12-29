class IpAndPortChecker:

    def __init__(self, summoner='программа', help_function=None, help_parameter='help'):
        self._help_parameter = help_parameter
        self._init_help_function(help_function)
        self._summoner = summoner

        self._max_value_ip = 255
        self._min_port = 1025
        self._max_port = 65535
        self._wrong_variable_mess = 'Вы неправильно указали переменные для запуска, ' \
                                    f'если вам требуется помощь для запуска {self._summoner}, ' \
                                    f'воспользуйтесь параметром {self._help_parameter}'
        self._wrong_ip_mess = 'Указан неверный IP адресс, IP адресс должен иметь вид X.X.X.X, ' \
                              'где каждый X это число от 0 - 255'
        self._wrong_port_mess = 'Порт для подключения должен быть числом в диапазоно 1025 - 65535'

    def _init_help_function(self, my_function):
        if not my_function:
            self._help_function = self._default_help_function
        elif my_function is function or my_function is classmethod:
            self._help_function = my_function
        else:
            print('В параметр help function была передана не функция')
            exit(1)

    def _default_help_function(self):
        print('help')

    def ejection_program(self, eject_type='main'):
        if eject_type == 'id':
            print(self._wrong_ip_mess)
        elif eject_type == 'port':
            print(self._wrong_port_mess)
        elif eject_type == 'main':
            print(self._wrong_variable_mess)
        else:
            print('eject_type был указан не верно, причина выхода не ясна')
        exit(1)

    # has unittest
    def check_ip_counts(self, count: int):
        if count <= self._max_value_ip:
            return True
        else:
            self.ejection_program(eject_type='ip')

    # has unittest
    def ip_split(self, ip: str, splitter: str):
        try:
            return ip.split(splitter)
        except AttributeError:
            self.ejection_program(eject_type='ip')

    # has unittest
    def ip_list_convert(self, ip):
        for index, item in enumerate(ip):
            try:
                new_item = int(item)
            except ValueError:
                self.ejection_program(eject_type='id')
            else:
                self.check_ip_counts(new_item)
                ip[index] = new_item
        return ip

    def pars_ip(self, ip: str):
        ip = self.ip_split(ip=ip, splitter='.')
        ip = self.ip_list_convert(ip=ip)
        return ip

    def check_ip(self, ip: str):
        """check is input a ip or some string. If input not ip, close client"""
        ip = self.pars_ip(ip)
        for value in ip:
            self.check_ip_counts(count=value)

    # has_unittest
    def check_port_range(self, port):
        if port is not int:
            try:
                port = int(port)
            except ValueError:
                self.ejection_program(eject_type='port')

        if self._min_port <= port <= self._max_port:
            return True
        else:
            self.ejection_program(eject_type='port')

    def check_port(self, port):
        """check is input a socket port or some string. If input not port, close client"""
        try:
            port = int(port)
        except ValueError:
            self.ejection_program(eject_type='port')

        self.check_port_range(port)

    # has unittest
    def get_index_sys_arg(self, key, my_system_args):
        try:
            index = my_system_args.index(key)
        except ValueError:
            return False
        else:
            return index

    def get_variable(self, my_system_args, index):
        try:
            new_var = my_system_args[index + 1]
        except IndexError:
            self.ejection_program()
        else:
            return new_var

    def check_new_var(self, key, new_var):
        if key == '-a':
            self.check_ip(new_var)
        elif key == '-p':
            self.check_port(new_var)
        return new_var

    def add_variables(self, my_system_args, my_variables):
        for key in my_variables.keys():
            if key in my_system_args:
                index = self.get_index_sys_arg(key=key, my_system_args=my_system_args)
                if not index:
                    continue

                new_var = self.get_variable(my_system_args=my_system_args, index=index)
                my_variables[key] = self.check_new_var(key=key, new_var=new_var)
        return my_variables

    def check_sys_args(self, my_system_args, my_variables):
        """check is input a right and set ip and host parameters
        -a  - is ip string
        -p  - is port number
        -un - is user name (for client)"""

        if len(my_system_args) == 2 and my_system_args[1] == 'help':
            self._help_function()
            exit(0)

        elif len(my_system_args) == 1:
            return my_variables

        else:
            my_variables = self.add_variables(my_system_args, my_variables)
        return my_variables


if __name__ == '__main__':
    import sys
    sys_args = sys.argv

    a = IpAndPortChecker('aaaaa')
    print(a.check_sys_args(sys_args, {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckina'}))
