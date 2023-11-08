import requests
from bs4 import BeautifulSoup
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
        print('ERROR {}'.format(response.status_code))
        return False  # если страницы нет

    def get_html(self):
        # if self._create_save_file():  # если файл существует, читаем с него данные
        #     with open(file='{}/{}/{}'.format(self.path, self.directori, self.filename), mode='r') as f:
        #         html = f.read()
        if True is False:
            pass
        else:  # если файла нет, вызываем _response_html и пишем его в файл
            html = self._response_html()
            if not html:
                return False  # если страницы нет
            # with open(file='{}/{}/{}'.format(self.path, self.directori, self.filename), mode='w') as f:
            #     f.write(html)
        return html


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def _cards(self):
        cards = self.soup.select_one('body'). \
            select_one('div.main'). \
            select_one('div.item_card').select('div.item')
        return cards

    def _row(self):
        result_rows = list()
        rows = self._cards()
        for row in rows:
            name = row.select_one('a.name_item').text.strip()
            descript = row.select_one('div.description')
            f = lambda x: x.text.split(': ')[-1].strip()
            brend, form, mass, mass_dir = list(map(f, descript.select('li')))
            price = row.select_one('p.price').text.strip()
            result_rows.append([name, brend, form, mass, mass_dir, price])
        return result_rows

    def run(self):
        result = self._row()
        return result


class CreatCSV:
    def __init__(self, head, rows):
        self.head = head
        self.rows = rows

    def run(self):
        with open(file='data.csv', mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(self.head)
            writer.writerows(self.rows)


def mane():
    result = list()
    url = 'https://parsinger.ru/html/index4_page_{}.html'
    num = 1
    while True:
        url_page = url.format(num)
        html = GetHtml(url=url_page).get_html()
        if not html:
            break
        page = Parser(html=html)
        result.extend(page.run())
        num += 1
    print(*result, sep='\n')
    head = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объем буферной памяти', 'Цена']
    CreatCSV(head=head, rows=result).run()


if __name__ == "__main__":
    mane()
