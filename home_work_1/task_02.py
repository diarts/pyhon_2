'''Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.'''

my_class = b'class'
my_function = b'function'
my_method = b'method'

print(f'У переменной my_development тип: {type(my_class)}, длина: {len(my_class)} и содержимое: {my_class}\n'
      f'У переменной my_development тип: {type(my_function)}, длина: {len(my_function)} и содержимое: {my_function}\n'
      f'У переменной my_development тип: {type(my_method)}, длина: {len(my_method)} и содержимое: {my_method}')