'''Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode ).'''


def decode(some_dict, encode=True):

    for key, value in some_dict.items():
        if encode:
            some_dict[key] = value.encode()
        else:
            some_dict[key] = value.decode()

def print_dict(some_dict):
    for key, value in some_dict.items():
        print(f'{key} - {value}', end='; ')
    print('\n')

my_dict = {
    'my_develop': 'разработка',
    'my_admin': 'администрирование',
    'my_protocol': 'protocol',
    'my_standart': 'standart',
}


decode(my_dict)
print_dict(my_dict)
decode(my_dict, False)
print_dict(my_dict)

