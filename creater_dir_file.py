import os
import requests
from fake_useragent import UserAgent


def f_ua():  # crate fake user agent
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    return fake_ua


def create_dir(name_dir: str) -> None:  # создаем, если ее нет директорию
    if os.path.exists(name_dir):
        print('Yes')
    else:
        print('No')
        os.mkdir(name_dir)


def record_file(url: str, name_dir: str, name_file: str) -> None:  # записываем файд
    path = f'{name_dir}/{name_file}.jpg'
    with open(path, 'wb') as file:
        response = requests.get(url=url, stream=True, headers=f_ua())
        for chunk in response.iter_content(chunk_size=100_000):
            file.write(chunk)
