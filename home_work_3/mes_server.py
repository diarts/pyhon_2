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
import select
from decorators.log_decorators import function_log
from loggers import server_logger as server_logger_source
from server_data import server_responce

server_logger = logging.getLogger('server_logger')
# for write check function logs in server log file, add file time rotating logger to check function logger
check_functions.ip_and_port_checker_logger.addHandler(server_logger_source.time_rotating_logger)


class JimServer:
    def __init__(self, socket_port, host, count_clients=1, m_transfering_bytes=2048, encoding='utf-8'):
        self._server_clients = []
        self._encoding = encoding
        self._m_transfer_b = m_transfering_bytes
        self._socket_port = socket_port
        self._host = host
        self._clients_count = count_clients
        self.json_decode_error = json.JSONDecodeError
        self._socket_timeout = 0.2
        self._chats_list = {}

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
    def open_tcp_socket(self):
        """function opened server socket and listen clients."""
        my_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_logger.debug(f'server socket bind to host = {self.get_host()}, port = {self.get_port()}')
        my_server_socket.bind((self.get_host(), self.get_port()))
        server_logger.debug(f'set socket listening client count = {self.get_client_count()}')
        my_server_socket.listen(self.get_client_count())
        server_logger.debug(f'set socket time out = {self.get_client_count()}')
        my_server_socket.settimeout(self._socket_timeout)
        return my_server_socket

    @function_log(server_logger)
    def get_client_mess(self, my_client):
        """function get message from the client"""
        return my_client.recv(self.get_m_transfering_b())

    @function_log(server_logger)
    def disconnect_client(self, my_client, disconnect_mess=''):
        """close link with client and deauthorize it"""
        server_logger.debug('send disconnect message to client')
        self.send_mess(my_client, disconnect_mess)
        server_logger.debug('remove client from server client list and close')
        self._server_clients.remove(my_client)
        my_client.close()
        server_logger.info('client is disconnected\n' + '_' * 100)

    @function_log(server_logger)
    def send_mess(self, my_client, mess):
        """send message to client"""
        my_client.send(mess.encode(self.get_encoding()))

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
    def work_with_chat(self, client, mess):
        room = mess.get('room')
        server_logger.debug(f'check is chat {room} exist')

        if not room:
            server_logger.error('in message with action join has not room name')
            self.send_mess(client, server_responce.wrong_request())
            return False
        else:
            server_logger.debug('check is room in chart list')
            if room not in self._chats_list:
                server_logger.debug(f'room with name {room} dose not exist in chats list, now that room been created')
                self._chats_list[room] = [client, ]
                server_logger.debug(f'now chats list is {self._chats_list}')
                server_logger.debug(f'sending accept required message to client {client}')
                self.send_mess(client, server_responce.accept_required(room))
                return True
            else:
                server_logger.debug(f'check is client in room {room}')
                if client not in self._chats_list[room]:
                    server_logger.debug('client not in room, now added')
                    self._chats_list[room].append(client)
                    self.send_mess(client, server_responce.accept_required(room))
                    return True
                else:
                    server_logger.error('client was in chat room')
                    self.send_mess(client, server_responce.client_alredy_connected())
                    return True

    @function_log(server_logger)
    def send_message_to_group(self,client, message, group_name):
        server_logger.debug(f'find chat with name: {group_name}')
        if group_name in self._chats_list:
            server_logger.debug(f'group name: {group_name} in chat list, start message sending loop')
            for chat_client in self._chats_list[group_name]:
                server_logger.debug(f'sending message for client of chat: {chat_client}')
                self.send_mess(chat_client, json.dumps(message))
            return True
        else:
            server_logger.debug(f'chat with name {group_name} not registered, send to client wrong request response')
            self.send_mess(client, server_responce.wrong_request(f' chat with name {group_name} not exist'))
            return False

    @function_log(server_logger)
    def client_send_message(self, message, client):
        server_logger.debug('get addressees of message')
        to_user = message.get('to')
        server_logger.debug('check addressees is exist')
        if not to_user:
            server_logger.debug('addressees is not exist, send to client wrong request response')
            self.send_mess(client, server_responce.wrong_request(' addressees in not exist'))
            return False

        server_logger.debug('addressees is group chat or user')
        if to_user[0] == '#':
            server_logger.debug('addressees is group chat')
            result = self.send_message_to_group(client, message, to_user[1:])
            return result
        else:
            server_logger.debug('addressees is user')
            return True


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

            elif action == "quit":
                server_logger.info('client request disconnect from server')
                server_logger.debug('value of action parameter is "quit", run disconnecting')
                self.disconnect_client(my_client, client_address)
                return "quit"

            elif action == "join":
                server_logger.info('client request join to chat room')
                result = self.work_with_chat(my_client, mess)
                if result:
                    return "join"
                else:
                    return None

            elif action == "msg":
                server_logger.info('client send message')
                result = self.client_send_message(mess, my_client)
                if not result:
                    return None
                else:
                    return "msg"

    @function_log(server_logger)
    def read_messages(self, read, address):
        requests = {}
        server_logger.debug('create requests dict')
        for client in read:
            server_logger.debug('getting client message')
            client_mess = self.get_client_mess(client)
            server_logger.debug('message is received, start processing')

            if not self.check_client_mess(client, address, client_mess):
                server_logger.debug('run next loop stage to getting client message')
                continue
            else:
                client_mess = self.decode_mess(client_mess, client, address)
                server_logger.debug('check is client message')
                if not client_mess:
                    server_logger.debug('client message is empty, run next loop stage to getting client message')
                    continue
                server_logger.debug('converting client message')
                client_mess = self.convert_mess(client_mess, client, address)
                server_logger.debug(f'converted is successful, message = {client_mess}')

                if not client_mess:
                    server_logger.debug('client message is empty, run next loop stage to getting client message')
                    continue

                server_logger.debug('add client mess to responses list')
                requests[client] = client_mess
                server_logger.debug('close client')
                server_logger.debug('remove client from server client list')
        return requests

    @function_log(server_logger)
    def write_message(self, write, responces, address):
        for client in write:
            if client in responces:
                mess = responces[client]
                server_logger.debug('run getting client action')
                result = self.work_whith_client_mess(mess, client, address)

    @function_log(server_logger)
    def server_work(self):
        """contains work server entirely"""
        server_logger.debug('opening tcp socket')
        server_socket = self.open_tcp_socket()
        server_logger.debug('opening is success')

        server_logger.debug('run an infinite loop to accept request for connection setting')
        while True:
            try:
                server_logger.info('server_socket accepting')
                client, address = server_socket.accept()
                server_logger.info('accepting successful')
            except OSError:
                pass
            else:
                server_logger.info(f'connecting to {client}, {address}...')
                self._server_clients.append(client)
                server_logger.debug('connecting is successful')
            finally:
                write = []
                read = []
                server_logger.debug(f'create write: {write} and read: {read} lists')

                try:
                    server_logger.debug('getting active read, write, e client lists')
                    read, write, e = select.select(self._server_clients, self._server_clients, [], 0)
                except Exception:
                    server_logger.warning('client disconnected')
                    pass
                else:
                    server_logger.debug(
                        f'getting active client lists is successful read: {read}, write: {write}, error: {e}')
                    request = self.read_messages(read, address)
                    self.write_message(write, request, address)


if __name__ == '__main__':
    server_logger.info('start application')
    ENCODING = 'utf-8'
    MAX_BYTES_TRANSFER = 2048
    MAX_CLIENTS = 10
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
