import requests
from fake_useragent import UserAgent
import os

# Выполняем GET-запрос к указанному URL с параметром stream=True.
# Параметр stream=True гарантирует, что соединение будет удерживаться, пока не будут получены все данные.
url = 'https://parsinger.ru/video_downloads/videoplayback.mp4'
path_file = 'file.mp4'

ua = UserAgent()
fake_ua = {'user-agent': ua.random}

response = requests.get(url=url, stream=True, headers=fake_ua)

# Открываем (или создаем) файл 'file.mp4' в режиме 'wb' (write binary),
# чтобы сохранить в него бинарные данные.
if response.status_code == 200:
    print('Good connect, statue code: {}'.format(response.status_code))
    if os.path.exists(path_file):
        print('Файл уже существует')
    else:
        print('Файла нет, идет запись..............')
        with open('file.mp4', 'wb') as file:
            # Записываем содержимое ответа (response.content) в файл.
            # Этот метод подходит для относительно небольших файлов,
            # так как все содержимое файла сначала загружается в оперативную память.
            for chunk in response.iter_content(chunk_size=100_000):
                file.write(chunk)
        if os.path.exists(path_file):
            print('Файл записан')
        else:
            print('ошибка при записи')
else:
    print('Bad connect, statue code: {}'.format(response.status_code))

file_size = os.path.getsize('file.mp4')
print('Размер файла:', file_size, 'байт')
