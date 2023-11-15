import bs4
import os
import json
import get_html

KEY = [
    "Наименование",
    "Бренд",
    "Форм-фактор",
    "Ёмкость",
    "Объем буферной памяти",
    "Цена",
]


class Parser:
    def __init__(self, html):
        self.soup = bs4.BeautifulSoup(html, 'lxml')

    def _cards(self):
        table = self.soup.select_one('body').select_one('div.main').select_one('div.item_card')
        cards = table.select('div.item')
        return cards

    def _row(self, card):
        name = card.select_one('a.name_item').text.strip()
        descriptions = card.select_one('div.description').select('li')
        descriptions = list(map(lambda x: x.text.split(': ')[-1].strip(), descriptions))
        price = card.select_one('div.container').select_one('p.price').text.strip()
        return [name, *descriptions, price]

    def run(self):
        rows = list()
        cards = self._cards()
        for card in cards:
            rows.append(self._row(card=card))
        return rows


def mane():
    json_list = list()
    rows_value = list()
    url = 'https://parsinger.ru/html/index4_page_{}.html'
    page = 1
    while True:
        page_url = url.format(page)
        html = get_html.GetHtml(url=page_url).get_html()
        if not html:
            break
        rows = Parser(html=html).run()
        rows_value.extend(rows)
        page += 1

    for row in rows_value:
        dc = dict(zip(KEY, row))
        json_list.append(dc)

    get_html.CreateJSON(ls=json_list).run()


if __name__ == "__main__":
    mane()
