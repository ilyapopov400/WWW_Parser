from bs4 import BeautifulSoup
import get_html


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def _cards(self):
        cards = self.soup.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select('div.item')
        return cards

    def _row(self, card):
        name = card.find(name='a', attrs={'class': 'name_item'}).text.strip()
        description = card.select_one('div.description').select('li')
        f = lambda x: x.text.strip().split(': ')[-1].strip()
        description = list(map(f, description))
        price = card.select_one('p.price').text.strip()
        row = [name, *description, price]

        return row

    def run(self):
        rows = list()
        cards = self._cards()
        for card in cards:
            row = self._row(card=card)
            rows.append(row)
        return rows


def mane():
    url = 'https://parsinger.ru/html/index{}_page_{}.html'
    result = list()
    for i in [1, 2, 3, 4, 5, ]:
        for j in [1, 2, 3, 4, ]:
            url_page = url.format(i, j)
            html = get_html.GetHtml(url=url_page).get_html()
            row = Parser(html=html).run()
            result.extend(row)

    head = []

    file_csv = get_html.CreatCSV(head=head, rows=result)
    file_csv.run()


if __name__ == "__main__":
    mane()
