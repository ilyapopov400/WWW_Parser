import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import json


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


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def _table(self):
        table = self.soup.select_one('body').find(name='table', attrs={'border': '1'})
        return table

    def _head(self, table) -> list:  # возвращаем заголовок таблицы
        head = table.find(name='thead').find(name='tr').find_all(name='th')
        head = list(map(lambda x: x.text.strip(), head))
        return head

    def _row(self, table):
        rows = table.find(name='tbody').find_all(name='tr')
        return rows

    def _filter(self, row):  # проверка списка на соответствие условию фильтрации
        if int(row[7]) > 4_000_000:
            return False
        if int(row[1]) < 2005:
            return False
        if row[4] != 'Бензиновый':
            return False
        return True

    def _new_head(self, row):  # выборка из списка необходимых позиций для окончательного словаря
        result = [row[0], row[1], row[4], row[7]]
        return result

    def run(self):
        result = list()
        table = self._table()
        head = self._head(table=table)
        head = self._new_head(row=head)

        rows = self._row(table=table)
        for row in rows:
            row = list(map(lambda x: x.text.strip(), row))
            if self._filter(row=row):
                row = self._new_head(row=row)
                row[1], row[3] = int(row[1]), int(row[3])
                row = dict(zip(head, row))
                result.append(row)

        # result = sorted(result, key=lambda x: x["Стоимость авто"])
        f_sort = lambda x: x[head[3]]
        result = sorted(result, key=f_sort)

        return result


def mane():
    url = 'https://parsinger.ru/4.8/6/index.html'

    html = GetHtml(url=url).get_html()
    a = Parser(html=html)
    cars = a.run()

    print(json.dumps(cars, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    mane()
