from bs4 import BeautifulSoup
import get_html


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
        name = card.select_one('#p_header').text.strip()
        article = card.select_one('p.article').text.split(': ')[-1].strip()
        brand = card.select_one('#brand').text.split(': ')[-1].strip()
        model = card.select_one('#model').text.split(': ')[-1].strip()
        in_stock = card.select_one('#in_stock').text.split(': ')[-1].strip()
        price = card.select_one('#price').text.split(': ')[-1].strip()
        old_price = card.select_one('#old_price').text.split(': ')[-1].strip()
        return [name, article, brand, model, in_stock, price, old_price, ]

    def run(self):
        row = self._row()
        return row


def get_result_list(url, parser) -> list:  # получаем список по url с использованием класса парсера
    result_list = list()
    type_product = 1
    while True:
        count_page = 1
        while True:
            page_url = url.format(type_product, count_page)
            html = get_html.GetHtml(url=page_url).get_html()
            if not html:
                type_product += 1
                count_page = 1
                break
            row = parser(html=html).run()
            result_list.extend(row)
            count_page += 1
        if not get_html.GetHtml(url=url.format(type_product, count_page)).get_html():
            break
    return result_list


def mane():
    url = 'https://parsinger.ru/html/index{}_page_{}.html'
    link_list = get_result_list(url=url, parser=ParserLink)
    prefics = 'https://parsinger.ru/html/'
    link_list = list(map(lambda x: prefics + x, link_list))  # список ссылок на отдельные карточки

    rows = list()
    for url in link_list:
        html = get_html.GetHtml(url=url).get_html()
        row = ParserCard(html=html).run()
        row.append(url)
        rows.append(row)

    head = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена', 'Ссылка']

    file_csv = get_html.CreatCSV(head=head, rows=rows)
    file_csv.run()


if __name__ == "__main__":
    mane()
