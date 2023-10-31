import requests
from bs4 import BeautifulSoup

from creater_dir_file import f_ua

url = 'https://parsinger.ru/4.8/3/index.html'


def get_html(url=url):
    header = f_ua()
    response = requests.get(url=url, headers=header)
    response.encoding = 'utf-8'
    if response:
        print(response.status_code)
        return response.text
    return False


class Parser:
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')

    def _get_table(self):
        table = self.soup.find(name='table', attrs={'border': '3'})
        print(table)


def mane():
    html = get_html(url=url)
    if html:
        result = Parser(html=html)
        result._get_table()
        print(result)
    else:
        print('ERROR')


mane()
