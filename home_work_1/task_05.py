'''Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.'''
import subprocess

ping = subprocess.Popen(['powershell.exe', 'ping yandex.ru; ping youtube.com'], stdout=subprocess.PIPE)
print(ping.stdout)
for string in ping.stdout:
    print(string.decode('cp866'))

