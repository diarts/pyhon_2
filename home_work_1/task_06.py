'''Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.'''
my_len = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w') as test_file:
    for i in my_len:
        test_file.write(i)

print(test_file)

with open('test_file.txt', 'br') as test_file:
    file = test_file.read()

print(file.decode(encoding='utf-8', errors='replace'))
