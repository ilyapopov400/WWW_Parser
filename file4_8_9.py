import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os


class GetHtml:
    '''
    получаем html в виде строки с использованием UserAgent
    '''

    def __init__(self, url):
        self.url = url
        self.path = os.getcwd()
        self.directori = 'datas_dir'  # имя директории и файла для хранения html
        self.filename = 'data.html'

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
        return 'ERROR {}'.format(response.status_code)

    def get_html(self):
        if self._create_save_file():  # если файл существует, читаем с него данные
            with open(file='{}/{}/{}'.format(self.path, self.directori, self.filename), mode='r') as f:
                html = f.read()
        else:  # если файла нет, вызываем _response_html и пишем его в файл
            html = self._response_html()
            with open(file='{}/{}/{}'.format(self.path, self.directori, self.filename), mode='w') as f:
                f.write(html)
        return html


def mane():
    url = 'https://parsinger.ru/4.8/6/index.html'

    html = GetHtml(url=url).get_html()
    print(html)
    # a = MyParser(html=html)
    # a.run()


if __name__ == "__main__":
    mane()
