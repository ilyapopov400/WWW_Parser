from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
import requests
import csv
import asyncio


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


class ParserLink:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def _cards(self):  # список карточек
        cards = self.soup.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select('div.item')
        return cards

    def _row(self, card):  # ссылка на отдельную карточку
        link = card.select_one('a.name_item').get('href').strip()
        return link

    def run(self):  # список ссылок на отдельные карточки
        cards = self._cards()
        rows = list(map(lambda x: self._row(card=x), cards))
        return rows


class ParserCard:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def _row(self):
        card = self.soup.select_one('div.description')
        name = card.select_one('#p_header').text.replace('Жесткий диск', '').strip()
        description = card.select_one('#description').select('li')
        f = lambda x: x.text.split(': ')[-1].strip()
        description = list(map(f, description))
        description = [description[0], *description[2:5], ]
        price = card.select_one('#price').text.strip()
        return [name, *description, price, ]

    def run(self):
        row = self._row()
        return row


def get_result_list(url, parser) -> list:  # получаем список по url с использованием класса парсера
    result_list = list()
    count_page = 1
    while True:
        page_url = url.format(count_page)
        html = GetHtml(url=page_url).get_html()
        if not html:
            break
        row = parser(html=html).run()
        result_list.extend(row)
        count_page += 1

    return result_list


def mane():
    url = 'https://parsinger.ru/html/index4_page_{}.html'
    link_list = get_result_list(url=url, parser=ParserLink)
    prefics = 'https://parsinger.ru/html/'
    link_list = list(map(lambda x: prefics + x, link_list))  # список ссылок на отдельные карточки

    rows = list()

    async def get_html(url):
        html = GetHtml(url=url).get_html()
        row = ParserCard(html=html).run()
        row.append(url)
        rows.append(row)

    async def mn():
        for url in link_list:
            task = asyncio.create_task(get_html(url=url))
            await task

    asyncio.run(mn())

    head = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объём буф. памяти', 'Цена']

    file_csv = CreatCSV(head=head, rows=rows)
    file_csv.run()


if __name__ == "__main__":
    mane()
