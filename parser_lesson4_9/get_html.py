import requests
from fake_useragent import UserAgent
import os
import csv


class GetHtml:
    '''
    получаем html в виде строки с использованием UserAgent
    '''

    def __init__(self, url):
        self.url = url
        self.path = os.getcwd()
        self.directori = 'datas_dir'  # имя директории и файла для хранения html
        self.filename = url.split('/')[-1]

    def _fake_user_agent(self):  # crate fake user agent
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        return fake_ua

    def _create_save_file(self):
        if not os.path.exists('{}/{}'.format(self.path, self.directori)):
            os.mkdir('{}/{}'.format(self.path, self.directori))

        if os.path.exists('{}/{}/{}'.format(self.path, self.directori, self.filename)):
            return True
        else:
            return False

    def _response_html(self) -> str:
        header = self._fake_user_agent()
        response = requests.get(url=self.url, headers=header)
        response.encoding = 'utf-8'
        if response:
            print(response.status_code)
            return response.text
        else:
            print('ERROR {}'.format(response.status_code))
            return False  # если страницы нет

    def get_html(self):
        if self._create_save_file():  # если файл существует, читаем с него данные
            with open(file='{}/{}/{}'.format(self.path, self.directori, self.filename), mode='r') as f:
                html = f.read()

        else:  # если файла нет, вызываем _response_html и пишем его в файл
            html = self._response_html()
            if not html:
                return False  # если страницы нет
            with open(file='{}/{}/{}'.format(self.path, self.directori, self.filename), mode='w') as f:
                f.write(html)
        return html


class CreatCSV:
    def __init__(self, head, rows):
        self.head = head
        self.rows = rows
        self.directori = 'datas_dir'  # имя директории и файла для хранения csv
        self.filename = 'data.csv'
        self.path = os.getcwd()

    def _create_save_directory(self):
        if not os.path.exists('{}/{}'.format(self.path, self.directori)):
            os.mkdir('{}/{}'.format(self.path, self.directori))

    def run(self):
        self._create_save_directory()
        path_dir = '{}/{}'.format(self.directori, self.filename)
        with open(file=path_dir, mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            if bool(self.head):
                writer.writerow(self.head)
            writer.writerows(self.rows)


def mane():
    url = 'https://parsinger.ru/html/index4_page_{}.html'
    num = 1
    while True:
        url_page = url.format(num)
        html = GetHtml(url=url_page).get_html()
        if not html:
            break
        print(num)
        num += 1


if __name__ == "__main__":
    mane()
