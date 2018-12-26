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

import socket
import time
import json


# ____________________  responce   _____________________________________

def accept_presence():
    mess = {
        "responce": 202,
        "alert": "connecting to server is successful"
    }
    return json.dumps(mess)


def wrong_request():
    mess = {
        "responce": 400,
        "error": "You request not compliant"
    }
    return json.dumps(mess)


def client_alredy_connected():
    mess = {
        "responce": 409,
        "error": "You already connected on server"
    }
    return json.dumps(mess)


# _________________________________________________________________________________

def get_u_time():
    return round(time.time())


def u_time_convert(u_time):
    return time.ctime(u_time)


def open_tcp_socket(port, host='', count_clients=1):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(count_clients)
    return server_socket


def get_client_mess(my_client, max_bytes_transfered):
    return my_client.recv(max_bytes_transfered)


def disconect_client(my_client, account_name, disconect_mess, clients_list, mess_encoding='utf-8'):
    send_mess(my_client, disconect_mess, mess_encoding)
    my_client.close()
    print(f'Клиент {my_client} был отключен \n' + '_'*100)
    item = check_client_is_autorize(account_name, clients_list)
    if item:
        client_deautorize(item, clients_list)


def check_client_mess(my_client, client_address, mess, client_list, mess_encoding='utf-8'):
    if not mess:
        print(f'connecting to {client_address} is failed')
        disconect_client(my_client, client_address, wrong_request(), client_list, mess_encoding)
        return False
    else:
        print(f'connecting to {client_address} is successful')
        return True


def send_mess(my_client, mess, mess_encoding):
    my_client.send(mess.encode(mess_encoding))


def decode_mess(mess, my_client, client_address, client_list, mess_encoding='utf-8'):
    try:
        decoding_mess = mess.decode(mess_encoding)
    except UnicodeDecodeError:
        print(f'сообщение от клиента {client_address} пришло в неправильной кодировке!')
        disconect_client(my_client, client_address, '', client_list, mess_encoding)
        return None
    else:
        return json.loads(decoding_mess)


def work_whith_client_mess(mess, my_client, client_address, client_list, mess_encoding):
    try:
        action = mess["action"]
    except KeyError:
        print(f'в сообщении клиента {client_address} отсутствовал параметр action')
        disconect_client(my_client, None, wrong_request(), client_list, mess_encoding)
    else:
        if action == "presence":
            client_presence(my_client, client_address, mess.get("user"), client_list, mess_encoding)
            return "presence"
        elif action == "quit":
            print('клиент запросил отключение')
            disconect_client(my_client, client_address, '', client_list)
            return "quit"


def client_presence(my_client, client_address, client_user, clients_list, mess_encoding):
    if not client_user or not client_user.get("account_name"):
        disconect_client(my_client, client_user.get("account_name"), wrong_request(), clients_list, mess_encoding)
    else:
        account_name = client_user.get("account_name")
        if check_client_is_autorize(account_name, clients_list):
            disconect_client(my_client, account_name, client_alredy_connected(), clients_list, mess_encoding)
        else:
            clients_list.append((client_address, account_name))
            send_mess(my_client, accept_presence(), mess_encoding)


def check_client_is_autorize(account_name, clients_list):
    for item in clients_list:
        if account_name in item:
            return item
    else:
        return False


def client_deautorize(item, clients_list):
    clients_list.remove(item)


if __name__ == '__main__':

    SOCKET_PORT = 7777
    COUNT_CLIENTS = 1
    ENCODING = 'utf-8'
    MAX_BYTES_TRANSFERED = 2048
    authorized_clients = []

    server_socket = open_tcp_socket(SOCKET_PORT, count_clients=COUNT_CLIENTS)
    client, address = server_socket.accept()
    print(f'connected to {address}...')

    while True:
        client, address = server_socket.accept()
        print(f'connected to {address}...')

        while True:
            client_mess = get_client_mess(client, MAX_BYTES_TRANSFERED)
            print(client_mess)
            if not check_client_mess(client, address, client_mess, authorized_clients, ENCODING):
                continue
            else:
                client_mess = decode_mess(client_mess, client, address, authorized_clients, ENCODING)
                if not client_mess:
                    continue

                result = work_whith_client_mess(client_mess, client, address, authorized_clients, ENCODING)
                if result == "quit":
                    break