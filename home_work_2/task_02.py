'''Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:

a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(i tem) , количество ( quantity) , цена ( price) , покупатель ( buyer) , дата ( date) . Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При
записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра.'''
import datetime
import json


def write_order_to_json(item='none', quantity='none', price='none', buyer='none', date='none'):
    INDENT = 4

    json_dict = {}
    json_dict['item'] = item
    json_dict['quantity'] = quantity
    json_dict['price'] = price
    json_dict['buyer'] = buyer
    json_dict['date'] = date

    for key, item in json_dict.items():
        if item is not str and item is not int and item is not bool:
            json_dict[key] = str(item)

    with open('orders.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_dict, json_file, indent=INDENT)


item = 'car'
quantity = 256
price = 84.65
buyer = 10658
time = datetime.datetime.now()

write_order_to_json(item=item, quantity=quantity, price=price, buyer=buyer, date=time)
