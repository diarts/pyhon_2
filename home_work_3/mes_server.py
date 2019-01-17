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

import inspect
import sys
import socket
import time
import json
import logging
import check_functions
from decorators.log_decorators import function_log
from loggers import server_logger as server_logger_source
from server_data import server_responce

server_logger = logging.getLogger('server_logger')
# for write check function logs in server log file, add file time rotating logger to check function logger
check_functions.ip_and_port_checker_logger.addHandler(server_logger_source.time_rotating_logger)


class JimServer:
    def __init__(self, socket_port, host, count_clients=1, m_transfering_bytes=2048, encoding='utf-8'):
        self._encoding = encoding
        self._m_transfer_b = m_transfering_bytes
        self._socket_port = socket_port
        self._host = host
        self._clients_count = count_clients
        self.json_decode_error = json.JSONDecodeError
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

    @function_log(server_logger)
    def get_encoding(self):
        return self._encoding

    @function_log(server_logger)
    def get_m_transfering_b(self):
        return self._m_transfer_b

    @function_log(server_logger)
    def get_port(self):
        return self._socket_port

    @function_log(server_logger)
    def get_host(self):
        return self._host

    @function_log(server_logger)
    def get_client_count(self):
        return self._clients_count

    @function_log(server_logger)
    def get_client_list(self):
        return self._clients_list

    @function_log(server_logger)
    def open_tcp_socket(self):
        """function opened server socket and listen clients."""
        my_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_logger.debug(f'server socket bind to host = {self.get_host()}, port = {self.get_port()}')
        my_server_socket.bind((self.get_host(), self.get_port()))
        server_logger.debug('set client listening count = {self.get_client_count()}')
        my_server_socket.listen(self.get_client_count())
        return my_server_socket

    @function_log(server_logger)
    def get_client_mess(self, my_client):
        """function get message from the client"""
        return my_client.recv(self.get_m_transfering_b())

    @function_log(server_logger)
    def disconnect_client(self, my_client, account_name, disconect_mess=''):
        """close link with client and deauthorize it"""
        server_logger.debug('send disconnect message to client')
        self.send_mess(my_client, disconect_mess)
        server_logger.debug('close client')
        my_client.close()
        server_logger.info('client is disconected\n' + '_' * 100)
        server_logger.debug('finding disconnect client in client list')
        item = self.find_client(account_name)
        if item:
            server_logger.debug('disconnect client be find, run deauthorize it')
            self.client_deauthorize(item)

    @function_log(server_logger)
    def authorize_client(self, client_address, account_name):
        self._clients_list.append((client_address, account_name))

    @function_log(server_logger)
    def find_client(self, account_name):
        """find client in authorize clients list"""
        server_logger.debug(f'run find client: {account_name}')
        for item in self.get_client_list():
            if account_name in item:
                server_logger.debug('client be find')
                return item
        else:
            server_logger.debug('client do not be find, deautorization not require')
            return False

    @function_log(server_logger)
    def client_deauthorize(self, item):
        """remove client from clients list"""
        self._clients_list.remove(item)

    @function_log(server_logger)
    def send_mess(self, my_client, mess):
        """send message to client"""
        my_client.send(mess.encode(self.get_encoding()))

    @function_log(server_logger)
    def client_presence(self, my_client, client_address, client_user):
        """check client is authorize and if it don't, authorize it"""
        server_logger.debug('check dose exist client user and dose it has account_name')
        if not client_user or not client_user.get("account_name"):
            server_logger.warning('client has not client user or has not account name')
            server_logger.debug('run disconnect client')
            self.disconnect_client(my_client, client_user.get("account_name"), server_responce.wrong_request())
            return False
        else:
            server_logger.debug('client has account_name')
            account_name = client_user.get("account_name")
            server_logger.debug('check is account already autorize or not')
            if self.find_client(account_name):
                server_logger.debug('account already autorize, run disconnecting')
                self.disconnect_client(my_client, account_name, server_responce.client_alredy_connected())
                return False
            else:
                server_logger.debug('account not be autorize, run autorisation')
                self.authorize_client(client_address, account_name)
                server_logger.debug('autorization is success, send accept presence message to client')
                self.send_mess(my_client, server_responce.accept_presence())
                return True

    @function_log(server_logger)
    def check_client_mess(self, my_client, client_address, mess):
        """check is client message. If client message is empty, disconect client"""
        if not mess:
            server_logger.debug('client message is empty, run disconnecting from client')
            server_logger.info(f'connecting to {client_address} is failed')
            self.disconnect_client(my_client, client_address, server_responce.wrong_request())
            return False
        else:
            server_logger.info(f'connecting to {client_address} is successful')
            return True

    @function_log(server_logger)
    def decode_mess(self, mess, my_client, client_address):
        """get client message and decoding it.
        If encoding of message don't equal of standard encoding server and client, client be disconnect"""

        server_logger.debug('run decode message')
        try:
            decoding_mess = mess.decode(self.get_encoding())
        except UnicodeDecodeError:
            server_logger.warning(f'message from client: {client_address} send with wrong encoding')
            server_logger.debug('run disconnect client')
            self.disconnect_client(my_client, client_address)
            return None
        else:
            server_logger.debug('decode is successful')
            return decoding_mess

    @function_log(server_logger)
    def convert_mess(self, mess, my_client, client_address):
        server_logger.debug('run convert json client message to dict')
        try:
            converted_mess = json.loads(mess)
        except self.json_decode_error:
            server_logger.warning(f'message from client: {client_address} send with wrong protocol type')
            server_logger.debug('run disconnect client')
            self.disconnect_client(my_client, client_address)
            return None
        else:
            server_logger.debug('convert is successful')
            return converted_mess

    @function_log(server_logger)
    def work_whith_client_mess(self, mess, my_client, client_address):
        """gets client action and starts match function"""
        server_logger.debug('try get parameter action')
        try:
            action = mess["action"]
        except KeyError:
            server_logger.warning(f'client message {mess} has not parameter action')
            server_logger.debug('run disconnect client')
            self.disconnect_client(my_client, None, server_responce.wrong_request())
            return False
        else:
            server_logger.debug('client message has parameter action, comparison it with "presence" and "quit"')
            if action == "presence":
                server_logger.debug('value of action parameter is "presence", run processing of presence message')
                answer = self.client_presence(my_client, client_address, mess.get("user"))
                if not answer:
                    return False
                else:
                    return "presence"
            elif action == "quit":
                server_logger.info('client request disconnect from server')
                server_logger.debug('value of action parameter is "quit", run disconnecting')
                self.disconnect_client(my_client, client_address)
                return "quit"

    @function_log(server_logger)
    def server_work(self):
        """contains work server entirely"""
        server_logger.debug('opening tcp socket')
        server_socket = self.open_tcp_socket()
        server_logger.debug('opening is success')

        server_logger.debug('run an infinite loop to accept request for connection setting')
        while True:
            client, address = server_socket.accept()
            server_logger.info(f'connecting to {address}...')

            server_logger.debug('run an infinite loop to getting client message and work with it')
            while True:
                server_logger.debug('getting client message')
                client_mess = self.get_client_mess(client)
                server_logger.debug('message is received, start processing')

                if not self.check_client_mess(client, address, client_mess):
                    server_logger.debug('run next loop stage to getting client message')
                    continue
                else:
                    client_mess = self.decode_mess(client_mess, client, address)
                    if not client_mess:
                        server_logger.debug('run next loop stage to getting client message')
                        continue
                    client_mess = self.convert_mess(client_mess, client, address)
                    if not client_mess:
                        server_logger.debug('run next loop stage to getting client message')
                        continue
                    server_logger.debug('run getting client action')
                    result = self.work_whith_client_mess(client_mess, client, address)
                    if not result:
                        break
                    elif result == "quit":
                        server_logger.debug('as result = quit, break infinite loop to getting client message')
                        break
                    else:
                        print('conversation')


if __name__ == '__main__':
    server_logger.info('start application')
    ENCODING = 'utf-8'
    MAX_BYTES_TRANSFER = 2048
    MAX_CLIENTS = 1
    my_variables = {'-a': '', '-p': 7777}

    server_logger.debug('getting system arguments')
    system_args = sys.argv
    server_logger.debug(f'system arguments is: {system_args}')

    checker = check_functions.IpAndPortChecker()
    variables = checker.check_sys_args(system_args, my_variables)

    server_logger.debug(f'create JimServer variable with parameters: ip address = {variables["-a"]}, '
                        f'port = {variables["-p"]}, max bytes transfer = {MAX_BYTES_TRANSFER}, '
                        f'max clients = {MAX_CLIENTS}, encoding = {ENCODING}')
    server = JimServer(variables['-p'], variables['-a'], MAX_CLIENTS, MAX_BYTES_TRANSFER, ENCODING)
    server_logger.info('starting server...')
    server.server_work()
    server_logger.info('close application')
