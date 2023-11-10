from bs4 import BeautifulSoup
import csv
import get_html


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')
        self.prefics = 'https://parsinger.ru/html/'

    def _cards(self):  # получаем карточки товара с главной страницы
        cards = self.soup.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select('div.item')
        return cards

    def _get_link(self, card):  # получаем ссылки на отдельные карточки
        result = card.select_one('a.name_item').get('href')
        return result

    def _description_date(self, description):  # разбираем description во внутренней карточки
        name = description.find(name='p', attrs={'id': 'p_header'}).text.strip()
        articul = description.find(name='p', attrs={'class': 'article'}).text.split(': ')[-1].strip()
        description_list = description.find(name='ul', attrs={'id': 'description'}).select('li')
        func = lambda x: x.text.split(': ')[-1].strip()
        description_list = list(map(func, description_list))
        in_stock = description.select_one('#in_stock').text.split(': ')[-1].strip()
        price = description.select_one('#price').text.strip()
        old_price = description.select_one('#old_price').text.strip()

        result = [name, articul, *description_list, in_stock, price, old_price]
        return result

    def _row(self, html) -> list:  # получаем список результирующих данных для таблицы из внутренней карточки
        card = BeautifulSoup(html, 'lxml')
        card = card.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select_one('div.description')
        result = self._description_date(description=card)

        return result

    def run(self):
        result = list()
        cards = self._cards()
        links = list(map(lambda x: self._get_link(x), cards))
        links = list(map(lambda x: self.prefics + x, links))
        for link in links:
            html = get_html.GetHtml(url=link).get_html()
            row = self._row(html)
            row.append(link)
            result.append(row)
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
    url = 'https://parsinger.ru/html/index1_page_{}.html'
    num = 1
    table_rows = list()
    while True:
        url_page = url.format(num)
        html = get_html.GetHtml(url=url_page).get_html()
        if not html:
            break
        page = Parser(html=html)
        result = page.run()
        table_rows.extend(result)
        num += 1

    head = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса',
            'Материал браслета', 'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена',
            'Ссылка на карточку с товаром']

    file_csv = CreatCSV(head=head, rows=table_rows)
    file_csv.run()


if __name__ == "__main__":
    mane()
