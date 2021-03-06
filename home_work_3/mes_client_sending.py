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
import inspect
import sys
import socket
import time
import json
import logging
import check_functions
from decorators.log_decorators import function_log
from loggers import client_logger as client_logger_source
from client_data import client_actions

client_logger = logging.getLogger('client_logger')
# for write check function logs in client log file, add file rotating logger to check function logger
check_functions.ip_and_port_checker_logger.addHandler(client_logger_source.file_rotating_logger)


class JimClient:
    chat_room = 'my_room'

    def __init__(self, socket_port, host, m_transfer_bytes=2048, type_of_client='sending', user_name='admin',
                 encoding='utf-8'):
        self._socket_port = socket_port
        self._m_transfer_b = m_transfer_bytes
        self._encoding = encoding
        self._host = host
        self._user_name = user_name
        self._type_of_client = type_of_client
        self.json_decode_error = json.JSONDecodeError

    @staticmethod
    def get_u_time():
        """function gets real time at unix time type"""
        return round(time.time())

    @staticmethod
    def u_time_convert(u_time):
        """function gets unix time and converts it in h.m.s. d.m.y type """
        return time.ctime(u_time)

    @function_log(client_logger)
    def get_socket_port(self):
        return self._socket_port

    @function_log(client_logger)
    def get_max_transfered_b(self):
        return self._m_transfer_b

    @function_log(client_logger)
    def get_encoding(self):
        return self._encoding

    @function_log(client_logger)
    def get_host(self):
        return self._host

    @function_log(client_logger)
    def get_user_name(self):
        return self._user_name

    @function_log(client_logger)
    def tcp_connect_to(self):
        """function connect client to server by specified port. If server is offline, client closed"""
        client_logger.debug('create client socket')
        my_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_logger.info(f'connecting to server...')
        client_logger.debug(f'try connect to server with host = {self.get_host()}, port = {self.get_socket_port()}')
        try:
            my_server_socket.connect((self.get_host(), self.get_socket_port()))
        except ConnectionRefusedError:
            client_logger.warning(f'connecting is failed, server not answer')
            return False
        client_logger.info(f'connecting is success')
        return my_server_socket

    @function_log(client_logger)
    def send_mess(self, my_socket, mess):
        """function sends specified message to the server"""
        client_logger.debug(f'sending message: {mess}')
        my_socket.send(mess.encode(self.get_encoding()))

    @function_log(client_logger)
    def get_server_mess(self, client_socket):
        """function get message from the server, decode it and convert to python dictionary.
        If it hasn't function responce or action, then client disconnect from the server"""
        server_message = client_socket.recv(self.get_max_transfered_b())
        client_logger.debug(f'server message received, start decode, encoding = {self.get_encoding()}')
        try:
            server_message = server_message.decode(self.get_encoding())
        except UnicodeEncodeError:
            client_logger.critical('server encoding different from client')
            return False
        try:
            client_logger.debug('converting json message to dict')
            server_message = json.loads(server_message)
        except self.json_decode_error:
            client_logger.critical('server message has wrong type')
            client_logger.debug('server message not in json type, decode error')
            return False

        client_logger.debug('find "responce" or "action" in server message')
        if "responce" not in server_message and "action" not in server_message:
            client_logger.critical('server message has wrong variables')
            client_logger.debug('server message has not responce or action variable')
            return False
        else:
            client_logger.debug('server message is right')
            return server_message

    @function_log(client_logger)
    def work_with_serv_mess(self, client_socket, mess):
        """call responce or action function request in dependence"""
        if not mess:
            client_logger.info('closing client')
            self.shutdown_from_serv(client_socket)

        client_logger.debug(f'server responce is: {mess}, getting responce or action')
        responce = mess.get("responce")
        action = mess.get("action")

        if responce:
            client_logger.debug('server message is responce type start processing for responce message')
            type_of_responce = self.work_with_responce(responce, mess)
            return type_of_responce

        elif action:
            client_logger.debug('server message is action type, start processing for action message')
            self.work_with_action(mess)

    @function_log(client_logger)
    def work_with_action(self, message):
        client_logger.debug(f'message = {message}')
        message_action = message.get('action')
        message_from = message.get('from')
        message_mesage = message.get('message')
        if message_action == 'msg':
            if message_from != self.get_user_name():
                print(f'{message_mesage} : от {message_from}')
            else:
                print(f'Я {message_from} написал : {message_mesage}')

    @function_log(client_logger)
    def work_with_responce(self, responce, mess):
        client_logger.debug(f'responce code = {responce}')
        if 100 < responce > 200:
            client_logger.debug('server responce type is "information"')
            client_logger.info(f'server message is: {mess.get("alert")}')
            return responce
        elif responce < 300:
            client_logger.debug(f'server message type is "request success": {mess.get("alert")}')
            return responce
        elif responce < 500:
            client_logger.debug(
                f'server message type is "the request cannot be executed, client error": {mess.get("error")}')
            return responce
        else:
            client_logger.debug(
                f'server message type is "the request cannot be executed, server error": {mess.get("error")}')
            return responce

    @function_log(client_logger)
    def shutdown_from_serv(self, my_client_socket):
        """send quit message to the server and close client"""
        client_logger.debug('send shutdown message to server')
        self.send_mess(my_client_socket, client_actions.quit_mess())
        client_logger.info('shutdown client from server, close client')
        my_client_socket.close()

    @function_log(client_logger)
    def sending_work(self, server_socket):
        client_logger.debug('start infinite loop fo sending message to group clients')
        while True:
            client_logger.debug('get message from user')
            message = input('Введите сообщение: ')
            if message == 'quit':
                client_logger.debug('work with server is finished')
                self.shutdown_from_serv(server_socket)
            else:
                print(f'{self.get_user_name()} написал: {message}')
                client_logger.debug(f'send {message} message to server')
                self.send_mess(server_socket,
                               client_actions.message(self.get_u_time(), self.chat_room, self.get_user_name(), message))

    @function_log(client_logger)
    def receiving_work(self, server_socket):
        client_logger.debug('start infinite loop fo receiving group client message')
        while True:
            client_logger.debug('getting group message from server')
            server_mess = self.get_server_mess(server_socket)
            responce = self.work_with_serv_mess(server_socket, server_mess)

    @function_log(client_logger)
    def start_client(self):
        """contains work client entirely"""
        client_logger.debug('create tcp connect to server')
        server_socket = self.tcp_connect_to()

        if not server_socket:
            client_logger.info('closing client')
            return False

        client_logger.debug(f'connecting to chat room: {self.chat_room}')
        self.send_mess(server_socket, client_actions.join_mess(self.get_u_time(), self.chat_room))
        client_logger.debug('getting server responce to connecting message')
        server_mess = self.get_server_mess(server_socket)
        responce = self.work_with_serv_mess(server_socket, server_mess)
        client_logger.debug(f'work with server responce: {responce}')

        if responce == 225:
            if self._type_of_client == 'sending':
                self.sending_work(server_socket)

            elif self._type_of_client == 'receiving':
                self.receiving_work(server_socket)

        elif responce == 202:
            client_logger.debug('client message responce code is 202, start conversation')
            for i in range(5):
                client_logger.info('conversation')

        client_logger.debug('work with server is finished')
        self.shutdown_from_serv(server_socket)


if __name__ == '__main__':
    client_logger.info('start application')
    MAX_BYTES_TRANSFER = 2048
    ENCODING = 'utf-8'
    my_variables = {'-a': 'localhost', '-p': 7777, '-un': 'Vasiliy Pupckin', '-type': 'sending'}

    system_args = sys.argv
    client_logger.debug(f'getting system arguments {system_args}')

    checker = check_functions.IpAndPortChecker()
    variables = checker.check_sys_args(system_args, my_variables)

    client_logger.debug(f'create JimClient variable with parameters: ip address = {variables["-a"]}, '
                        f'port = {variables["-p"]}, user_name = {variables["-un"]}, '
                        f'max bytes transfer = {MAX_BYTES_TRANSFER}, encoding = {ENCODING}, '
                        f'client type = {variables["-type"]}')

    client = JimClient(variables['-p'], variables['-a'], m_transfer_bytes=MAX_BYTES_TRANSFER,
                       user_name=variables['-un'], type_of_client=variables['-type'], encoding=ENCODING)

    client_logger.info('starting client')
    client.start_client()
    client_logger.info('close application')
