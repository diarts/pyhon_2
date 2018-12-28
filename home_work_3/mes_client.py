'''Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant
messaging):
a. клиент отправляет запрос серверу;
b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих
соответствующие функции. Для клиента:
● сформировать presence-сообщение;
● отправить сообщение серверу;
● получить ответ сервера;
● разобрать сообщение сервера;
● параметры командной строки скрипта client.py <addr> [<port>] :
○ addr — ip-адрес сервера;
○ port — tcp-порт на сервере, по умолчанию 7777.
'''
import sys
import socket
import time
import json
import check_functions
from client_data import client_actions


class JimClient:
    def __init__(self, socket_port, host, m_transfer_bytes=2048, user_name='admin', encoding='utf-8'):
        self._socket_port = socket_port
        self._m_transfer_b = m_transfer_bytes
        self._encoding = encoding
        self._host = host
        self._user_name = user_name

    def __del__(self):
        print('Отключение клиента')

    @staticmethod
    def get_u_time():
        """function gets real time at unix time type"""
        return round(time.time())

    @staticmethod
    def u_time_convert(u_time):
        """function gets unix time and converts it in h.m.s. d.m.y type """
        return time.ctime(u_time)

    def get_socket_port(self):
        return self._socket_port

    def get_max_transfered_b(self):
        return self._m_transfer_b

    def get_encoding(self):
        return self._encoding

    def get_host(self):
        return self._host

    def get_user_name(self):
        return self._user_name

    def tcp_connect_to(self):
        """function connect client to server by specified port. If server is offline, client closed"""
        my_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            my_client_socket.connect((self.get_host(), self.get_socket_port()))
        except ConnectionRefusedError:
            print('Connecton failed, server is offline')
            exit(0)
        return my_client_socket

    def send_mess(self, my_socket, mess):
        """function sends specified message to the server"""
        my_socket.send(mess.encode(self.get_encoding()))

    def get_server_mess(self, client_socket):
        """function get message from the server, decode it and convert to python dictionary.
        If it hasn't function responce or action, then client disconnect from the server"""
        server_message = client_socket.recv(self.get_max_transfered_b())
        server_message = server_message.decode(self.get_encoding())
        server_message = json.loads(server_message)

        if "responce" not in server_message and "action" not in server_message:
            print('сообщение от сервера пришло с неправильной структурой')
            self.shutdown_from_serv(client_socket)
        else:
            return server_message

    def work_with_serv_mess(self, mess):
        """call responce or action function request in dependence"""
        responce = mess.get("responce")
        action = mess.get("action")

        if responce:
            return self.work_with_responce(responce, mess)

    def work_with_responce(self, responce, mess):
        """print servers message by responce code"""
        if 100 < responce > 200:
            print('сервер прислал информационное сообщение: ' + mess.get("alert"))
            return responce
        elif responce < 300:
            print('запрос выполнен успешно, ' + mess.get("alert"))
            return responce
        elif responce < 500:
            print('сервер не может выполнить запрос, ошибка клиента: ' + mess.get("error"))
            return responce
        else:
            print('сервер не может выполнить запрос, ошибка сервера: ' + mess.get("error"))
            return responce

    def shutdown_from_serv(self, my_client_socket):
        """send quit message to the server and close client"""
        self.send_mess(my_client_socket, client_actions.quit_mess())
        print('отключение клиента от сервера')
        my_client_socket.close()

    def start_client(self):
        """contains work client entirely"""
        client_socket = self.tcp_connect_to()
        self.send_mess(client_socket, client_actions.presence_mess(self.get_user_name(), self.get_u_time()))
        server_mess = self.get_server_mess(client_socket)
        result = self.work_with_serv_mess(server_mess)

        if result == 202:
            for i in range(5):
                print('переписываемся')

        self.shutdown_from_serv(client_socket)

    @staticmethod
    def check_sys_args(my_system_args):
        """check is input a right and set ip, host and user name parameters
        -a  - is ip string
        -p  - is port number
        -un - is user name"""
        wrong_variables = 'Вы неправильно указали переменные для запуска, если вам требуется помощь ' \
                          'для запуска клиента, воспользуйтесь параметром help'
        my_variables = {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckin'}

        if len(my_system_args) == 2 and my_system_args[1] == 'help':
            print('help')
            exit(0)

        elif len(my_system_args) == 1:
            return my_variables

        elif '-a' in my_system_args or '-p' in my_system_args or '-un' in my_system_args:
            for item in my_variables.keys():
                try:
                    index = my_system_args.index(item)
                except ValueError:
                    continue

                try:
                    new_var = my_system_args[index + 1]
                except IndexError:
                    print(wrong_variables)
                    exit(1)

                if item == '-a':
                    check_functions.check_ip(new_var)
                elif item == '-p':
                    check_functions.check_port(new_var)

                my_variables[item] = new_var
            return my_variables
        else:
            print(wrong_variables)
            exit(1)


if __name__ == '__main__':
    system_args = sys.argv
    MAX_BYTES_TRANSFER = 2048
    ENCODING = 'utf-8'

    variables = JimClient.check_sys_args(system_args)
    client = JimClient(variables['-p'], variables['-a'], m_transfer_bytes=MAX_BYTES_TRANSFER,
                       user_name=variables['-un'], encoding=ENCODING)
    client.start_client()
