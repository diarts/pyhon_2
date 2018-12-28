'''Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant
messaging):
a. клиент отправляет запрос серверу;
b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих
соответствующие функции. Для сервера:
● принимает сообщение клиента;
● формирует ответ клиенту;
● отправляет ответ клиенту;
● имеет параметры командной строки:
○ -p <port> — TCP-порт для работы (по умолчанию использует 7777);
○ -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все
доступные адреса).'''

import sys
import socket
import time
import json
import check_functions
from server_data import server_responce


class JimServer:
    def __init__(self, socket_port, host, count_clients=1, m_transfering_bytes=2048, encoding='utf-8'):
        self._encoding = encoding
        self._m_transfer_b = m_transfering_bytes
        self._socket_port = socket_port
        self._host = host
        self._clients_count = count_clients
        self._clients_list = []

    def __del__(self):
        print('Выключение сервера')

    @staticmethod
    def get_u_time():
        """function gets real time at unix time type"""
        return round(time.time())

    @staticmethod
    def u_time_convert(u_time):
        """function gets unix time and converts it in h.m.s. d.m.y type """
        return time.ctime(u_time)

    def get_encoding(self):
        return self._encoding

    def get_m_transfering_b(self):
        return self._m_transfer_b

    def get_port(self):
        return self._socket_port

    def get_host(self):
        return self._host

    def get_client_count(self):
        return self._clients_count

    def get_client_list(self):
        return self._clients_list

    def open_tcp_socket(self):
        """function opened server socket and listen clients."""
        my_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_server_socket.bind((self.get_host(), self.get_port()))
        my_server_socket.listen(self.get_client_count())
        return my_server_socket

    def get_client_mess(self, my_client):
        """function get message from the client"""
        return my_client.recv(self.get_m_transfering_b())

    def disconnect_client(self, my_client, account_name, disconect_mess=''):
        """close link with client and deauthorize it"""
        self.send_mess(my_client, disconect_mess)
        my_client.close()
        print(f'Клиент {my_client} был отключен \n' + '_' * 100)
        item = self.find_client(account_name)
        if item:
            self.client_deauthorize(item)

    def authorize_client(self, client_address, account_name):
        self._clients_list.append((client_address, account_name))

    def find_client(self, account_name):
        """find client in authorize clients list"""
        for item in self.get_client_list():
            if account_name in item:
                return item
        else:
            return False

    def client_deauthorize(self, item):
        """remove client from clients list"""
        self._clients_list.remove(item)

    def send_mess(self, my_client, mess):
        """send message to client"""
        my_client.send(mess.encode(self.get_encoding()))

    def client_presence(self, my_client, client_address, client_user):
        """check client is authorize and if it don't, authorize it"""
        if not client_user or not client_user.get("account_name"):
            self.disconnect_client(my_client, client_user.get("account_name"), server_responce.wrong_request())
        else:
            account_name = client_user.get("account_name")
            if self.find_client(account_name):
                self.disconnect_client(my_client, account_name, server_responce.client_alredy_connected())
            else:
                self.authorize_client(client_address, account_name)
                self.send_mess(my_client, server_responce.accept_presence())

    def check_client_mess(self, my_client, client_address, mess):
        """check is client message. If client message is empty, disconect client"""
        if not mess:
            print(f'connecting to {client_address} is failed')
            self.disconnect_client(my_client, client_address, server_responce.wrong_request())
            return False
        else:
            print(f'connecting to {client_address} is successful')
            return True

    def decode_mess(self, mess, my_client, client_address):
        """get client message and decoding it.
        If encoding of message don't equal of standard encoding server and client, client be disconnect"""
        try:
            decoding_mess = mess.decode(self.get_encoding())
        except UnicodeDecodeError:
            print(f'сообщение от клиента {client_address} пришло в неправильной кодировке!')
            self.disconnect_client(my_client, client_address)
            return None
        else:
            return json.loads(decoding_mess)

    def work_whith_client_mess(self, mess, my_client, client_address):
        """gets client action and starts match function"""
        try:
            action = mess["action"]
        except KeyError:
            print(f'в сообщении клиента {client_address} отсутствовал параметр action')
            self.disconnect_client(my_client, None, server_responce.wrong_request())
        else:
            if action == "presence":
                self.client_presence(my_client, client_address, mess.get("user"))
                return "presence"
            elif action == "quit":
                print('клиент запросил отключение')
                self.disconnect_client(my_client, client_address)
                return "quit"

    def server_work(self):
        """contains work server entirely"""
        server_socket = self.open_tcp_socket()

        while True:
            client, address = server_socket.accept()
            print(f'connected to {address}...')

            while True:
                client_mess = self.get_client_mess(client)

                if not self.check_client_mess(client, address, client_mess):
                    continue
                else:
                    client_mess = self.decode_mess(client_mess, client, address)
                    print(client_mess)
                    if not client_mess:
                        continue

                    result = self.work_whith_client_mess(client_mess, client, address)
                    if result == "quit":
                        break

    @staticmethod
    def check_sys_args(my_system_args):
        """check is input a right and set ip and host parameters
        -a  - is ip string
        -p  - is port number"""
        wrong_variables = 'Вы неправильно указали переменные для запуска, если вам требуется помощь ' \
                          'для запуска сервера, воспользуйтесь параметром help'
        my_variables = {'-a': '', '-p': 7777}

        if len(my_system_args) == 2 and my_system_args[1] == 'help':
            print('help')
            exit(0)

        elif len(my_system_args) == 1:
            return my_variables

        elif '-a' in my_system_args or '-p' in my_system_args:
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
                else:
                    check_functions.check_port(new_var)

                my_variables[item] = new_var
            return my_variables
        else:
            print(wrong_variables)
            exit(1)


if __name__ == '__main__':
    system_args = sys.argv
    ENCODING = 'utf-8'
    MAX_BYTES_TRANSFERED = 2048
    MAX_CLIENTS = 1

    variables = JimServer.check_sys_args(system_args)
    print(variables)

    server = JimServer(variables['-p'], variables['-a'], MAX_CLIENTS, MAX_BYTES_TRANSFERED, ENCODING)
    server.server_work()
