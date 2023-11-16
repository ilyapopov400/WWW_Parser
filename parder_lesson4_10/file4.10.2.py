import bs4
import get_html

KEY = ["Наименование",
       "Бренд",
       "Тип",
       "Материал корпуса",
       "Технология экрана",
       "Цена",
       ]


class Parser:
    def __init__(self, html):
        self.soup = bs4.BeautifulSoup(markup=html, features='lxml')

    def _cards(self):
        table = self.soup.select_one('body').select_one('div.main').select_one('div.item_card')
        cards = table.select('div.item')
        return cards

    def _row(self, card):
        name = card.select_one('a.name_item').text.strip()
        descriptions = card.select_one('div.description').select('li')
        descriptions_value = list(map(lambda x: x.text.split(': ')[-1].strip(), descriptions))
        descriptions_key = list(map(lambda x: x.text.split(': ')[0].strip(), descriptions))
        price = card.select_one('div.container').select_one('p.price').text.strip()

        key = [KEY[0], *descriptions_key, KEY[-1]]
        result = dict(zip(key, [name, *descriptions_value, price]))
        return result

    def run(self):
        rows = list()
        cards = self._cards()
        for card in cards:
            rows.append(self._row(card=card))
        return rows


def mane():
    json_list = list()
    rows_value = list()
    url = 'https://parsinger.ru/html/index{}_page_{}.html'
    type_product = 1
    while True:
        page = 1
        while True:
            page_url = url.format(type_product, page)
            html = get_html.GetHtml(url=page_url).get_html()
            if not html:
                type_product += 1
                page = 1
                break
            rows = Parser(html=html).run()
            rows_value.extend(rows)
            page += 1
        if not get_html.GetHtml(url=url.format(type_product, page)).get_html():
            break

    for row in rows_value:
        json_list.append(row)

    print('len of json_list:', len(json_list))
    get_html.CreateJSON(ls=json_list).run()


if __name__ == "__main__":
    mane()
