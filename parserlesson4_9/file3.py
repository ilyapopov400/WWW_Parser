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
        self.result_list = list()

    def _get_table(self):
        table = self.soup.find(name='table', attrs={'border': '3'})
        return table

    def _get_head_body(self, table):
        rows = list(table.children)
        rows = list(filter(lambda x: len(x) > 1, rows))

        head = rows[0]
        head = head.find_all(name='th')
        head = [i.text for i in head]

        body = rows[1:]

        return head, body

    def _run(self):
        table = self._get_table()
        head = self._get_head_body(table=table)[0]
        body = self._get_head_body(table=table)[1]
        # body = list(map(lambda x: list(x.children), body))
        # row_body = list(filter(lambda x: len(x) > 1, body))
        row_body = list()

        for i in body:
            a = i.find_all(('td', 'th'))
            print(*a, sep='\n*******\n')
            [print(len(x), x.text) for x in a]
            break
            a = list(filter(lambda x: len(x) > 1, a))
            row_body.append(a)

            print(*a, sep='\n*******\n')
            print('&&&&&&&&')


    def __call__(self):
        self._run()


def mane():
    html = get_html(url=url)
    if html:
        result = Parser(html=html)
        result()
    else:
        print('ERROR')


mane()
