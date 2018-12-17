'''Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
байтовом типе.'''

my_attribute = 'attribute'.encode()
my_class ='класс'.encode()
my_function = 'функция'.encode()
my_type = 'type'.encode()


print(my_attribute, my_class, my_function, my_type)
print('невозможно записать в байтовом формате слова: attribute и type')