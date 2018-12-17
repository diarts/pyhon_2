'''Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных.'''

my_development = 'разработка'
my_socket = 'сокет'
my_decorator = 'декоратор'

print(f'У переменной my_development тип: {type(my_development)} и содержимое: {my_development}\n'
      f'У переменной my_development тип: {type(my_decorator)} и содержимое: {my_decorator}\n'
      f'У переменной my_development тип: {type(my_socket)} и содержимое: {my_socket}\n' + '-'*50)

b_my_development = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
b_my_socket = b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'
b_my_decorator = b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'

print(f'У переменной my_development тип: {type(b_my_development)} и содержимое: {b_my_development}\n'
      f'У переменной my_development тип: {type(b_my_decorator)} и содержимое: {b_my_decorator}\n'
      f'У переменной my_development тип: {type(b_my_socket)} и содержимое: {b_my_socket}')