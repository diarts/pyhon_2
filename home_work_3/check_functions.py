def check_ip(ip):
    """check is input a ip or some string. If input not ip, close client"""
    wrong_ip = 'Указан неверный IP адресс, IP адресс должен иметь вид X.X.X.X, где каждый X это число от 0 - 255'
    ip = ip.split('.')

    if len(ip) == 4:
        for num in ip:
            try:
                num = int(num)
            except ValueError:
                print(wrong_ip)
                exit(1)

            if num <= 255:
                continue
            else:
                print(wrong_ip)
                exit(1)
        else:
            return True
    else:
        print(wrong_ip)
        exit(1)

def check_port(port):
    """check is input a socket port or some string. If input not port, close client"""
    try:
        port = int(port)
    except ValueError:
        print('Порт для подключения должен быть числом в диапазоно 1025 - 65535')
        exit(1)

    if 1024 < port <= 65535:
        return True
    else:
        print('Указанный порт не входит в диапазон доступных портов: 1025 - 65535')
        exit(1)