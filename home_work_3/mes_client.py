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

import socket
import time
import json


# _________________  actions   ___________________________________________

def presence_mess(account_name, time_connect):
    mess = {
        "action": "presence",
        "time": time_connect,
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "i am connect!"
        }
    }
    return json.dumps(mess)


def quit_mess():
    mess = {
        "action": "quit"
    }
    return json.dumps(mess)


# _________________________________________________________________________

def get_u_time():
    return round(time.time())


def u_time_convert(u_time):
    return time.ctime(u_time)


def tcp_connect_to(port, host='localhost'):
    my_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_client_socket.connect((host, port))
    except ConnectionRefusedError:
        print('Connecton failed, server is offline')
        exit(0)
    return my_client_socket


def send_mess(my_socket, mess, mess_encoding):
    my_socket.send(mess.encode(mess_encoding))


def get_server_mess(max_bytes_transfered, mess_encoding):
    server_message = client_socket.recv(max_bytes_transfered)
    server_message = server_message.decode(mess_encoding)
    server_message = json.loads(server_message)

    if "responce" not in server_message and "action" not in server_message:
        print('сообщение от сервера пришло с неправильной структурой')
        shutdown_from_serv(client_socket, mess_encoding)
    else:
        return server_message


def work_with_serv_mess(mess):
    responce = mess.get("responce")
    action = mess.get("action")

    if responce:
        return work_with_responce(responce, mess)


def work_with_responce(responce, mess):
    print(mess)
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


def shutdown_from_serv(my_client_socket, mess_encoding):
    send_mess(my_client_socket, quit_mess(), mess_encoding)
    print('отключение соединения клиента')
    client_socket.close()


if __name__ == '__main__':
    SOCKET_PORT = 7777
    MAX_BYTES_TRANSFERED = 204800
    ENCODING = 'utf-8'

    client_socket = tcp_connect_to(SOCKET_PORT)
    send_mess(client_socket, presence_mess('admin', get_u_time()), ENCODING)
    server_mess = get_server_mess(MAX_BYTES_TRANSFERED, ENCODING)

    result = work_with_serv_mess(server_mess)
    if result == 202:
        print('переписываемся')
    time.sleep(6)
    shutdown_from_serv(client_socket, ENCODING)
