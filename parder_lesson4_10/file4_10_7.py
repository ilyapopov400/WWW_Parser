import bs4
import requests
from fake_useragent import UserAgent
import os
import json
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


class CreateJSON:
    def __init__(self, ls: list):
        self.path = os.getcwd()
        self.ls = ls
        self.directori = 'datas_json'  # имя директории и файла для хранения json
        self.filename = 'data.json'

    def _create_save_directory(self):
        if not os.path.exists('{}/{}'.format(self.path, self.directori)):
            os.mkdir('{}/{}'.format(self.path, self.directori))

    def run(self):
        self._create_save_directory()
        path_dir = '{}/{}'.format(self.directori, self.filename)
        with open(file=path_dir, mode='w', encoding='utf-8-sig') as file:
            json.dump(self.ls, file, indent=4, ensure_ascii=False)


class ParserLink:
    def __init__(self, html):
        self.soup = bs4.BeautifulSoup(markup=html, features="lxml")

    def _cards(self):
        cards = self.soup.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select('div.item')
        return cards

    def run(self):
        cards = self._cards()
        date_list = list()
        for card in cards:
            date = card.select_one('div.img_box').select_one('a.name_item').get('href')
            date_list.append(date)
        return date_list


class ParserCard:
    def __init__(self, html, url):
        self.soup = bs4.BeautifulSoup(markup=html, features="lxml")
        self.url = url

    def run(self):
        result_dict = dict()
        card = self.soup.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select_one('div.description')

        result_dict["categories"] = self.url.split('://')[1].split('/')[2].strip()
        result_dict["name"] = card.select_one('#p_header').text.strip()
        result_dict["article"] = card.select_one('p.article').text.split(': ')[-1].strip()

        key = map(lambda x: x.get('id'), card.select_one('#description').select('li'))
        value = map(lambda x: x.text.split(': ')[1].strip(), card.select_one('#description').select('li'))
        result_dict["description"] = dict(zip(key, value))

        result_dict["count"] = card.select_one('#in_stock').text.split(': ')[-1].strip()
        result_dict["price"] = card.select_one('#price').text.strip()
        result_dict["old_price"] = card.select_one('#old_price').text.strip()
        result_dict["link"] = self.url

        return result_dict


def get_dates(url: str, parser) -> list:  # пробегаем по страницам и собираем данные в список
    dates_list = list()
    index_page = 1  # выбираем категорию товара
    while True:
        page = 1
        while True:
            page_url = url.format(index_page, page)
            html = GetHtml(url=page_url).get_html()
            if not html:
                index_page += 1
                page = 1
                break
            page += 1
            link = parser(html=html).run()
            dates_list.extend(link)
        break  # отрабатываем только одну заданную категорию index_page
        if not GetHtml(url=url.format(index_page, page)).get_html():
            break
    return dates_list


def mane():
    url = 'https://parsinger.ru/html/index{}_page_{}.html'

    cards_link = get_dates(url=url, parser=ParserLink)
    cards_link = list(map(lambda x: 'https://parsinger.ru/html/' + x, cards_link))  # собрали линки карточек

    json_list = list()

    for url in cards_link:
        html = GetHtml(url=url).get_html()
        if not html:
            print('битая ссылка: ', url)
        else:
            data_card = ParserCard(html=html, url=url).run()
            json_list.append(data_card)

    CreateJSON(ls=json_list).run()


if __name__ == "__main__":
    mane()
