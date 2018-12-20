'''Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов i nfo_1.txt, i nfo_2.txt, i nfo_3.txt и формирующий новый
«отчетный» файл в формате CSV . Для этого:

a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);

b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data() , а также
сохранение подготовленных данных в соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv() .'''

import re
import csv


def get_value(my_string):
    re_pattern = r'^.*:\s*'
    return re.split(re_pattern, my_string)


def get_data(file_list):
    main_data = [['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы']]

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for file in file_list:
        try:
            with open(file, 'r', encoding='windows-1251') as open_file:
                for line in open_file:
                    if 'Изготовитель ОС' in line:
                        value_list = get_value(line)
                        os_prod_list.append(value_list[1].rstrip())
                    elif 'Название ОС' in line:
                        value_list = get_value(line)
                        os_name_list.append(value_list[1].rstrip())
                    elif 'Код продукта' in line:
                        value_list = get_value(line)
                        os_code_list.append(value_list[1].rstrip())
                    elif 'Тип системы' in line:
                        value_list = get_value(line)
                        os_type_list.append(value_list[1].rstrip())
        except FileNotFoundError:
            print(f'файла {file} не существует')

    max_len = max(len(os_code_list), len(os_name_list), len(os_prod_list), len(os_type_list))

    for count in range(max_len):
        try:
            new_main_data_list = []
            new_main_data_list.append(os_prod_list[count])
            new_main_data_list.append(os_name_list[count])
            new_main_data_list.append(os_code_list[count])
            new_main_data_list.append(os_type_list[count])
        except IndexError:
            print('Недостает значений для одного из параметров')

        main_data.append(new_main_data_list)

    return main_data


def write_to_csv(file_url):
    file_list = ['info_1.txt', 'info_3.txt', 'info_2.txt']

    data = get_data(file_list)

    with open(file_url, 'w', encoding='utf-8') as written_file:
        my_writer = csv.writer(written_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            my_writer.writerow(row)


write_to_csv('my_csv.csv')