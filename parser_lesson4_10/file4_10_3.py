import bs4
import get_html

KEY = ["categories",
       "name",
       "article",
       "description",
       "count",
       "price",
       "old_price",
       "link"
       ]


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
    def __init__(self, html):
        self.soup = bs4.BeautifulSoup(markup=html, features="lxml")

    def run(self):
        result_dict = dict()
        card = self.soup.select_one('body').select_one('div.main'). \
            select_one('div.item_card').select_one('div.description')
        result_dict["categories"] = "mobile"
        result_dict["name"] = card.select_one('#p_header').text.strip()
        result_dict["article"] = card.select_one('p.article').text.split(': ')[-1].strip()
        key = ["brand",
               "model",
               "type",
               "material",
               "type_display",
               "diagonal",
               "size",
               "weight",
               "resolution",
               "site", ]
        value = map(lambda x: x.text.split(': ')[1].strip(), card.select_one('#description').select('li'))
        result_dict["description"] = dict(zip(key, value))
        result_dict["count"] = card.select_one('#in_stock').text.split(': ')[-1].strip()
        result_dict["price"] = card.select_one('#price').text.strip()
        result_dict["old_price"] = card.select_one('#old_price').text.strip()

        return result_dict


def get_dates(url: str, parser) -> list:  # пробегаем по страницам и собираем данные в список
    page = 1
    dates_list = list()
    while True:
        page_url = url.format(page)
        html = get_html.GetHtml(url=page_url).get_html()
        if not html:
            break
        page += 1
        link = parser(html=html).run()
        dates_list.extend(link)
    return dates_list


def mane():
    url = 'https://parsinger.ru/html/index2_page_{}.html'

    cards_link = get_dates(url=url, parser=ParserLink)
    cards_link = list(map(lambda x: 'https://parsinger.ru/html/' + x, cards_link))  # собрали линки карточек

    json_list = list()
    for url in cards_link:
        html = get_html.GetHtml(url=url).get_html()
        if not html:
            print('битая ссылка: ', url)
        data_card = ParserCard(html=html).run()
        data_card["link"] = url

        json_list.append(data_card)

    get_html.CreateJSON(ls=json_list).run()


if __name__ == "__main__":
    mane()
