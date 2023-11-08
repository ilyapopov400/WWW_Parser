from bs4 import BeautifulSoup

from parser_lesson4_8.file4 import GetHtml, Parser

url = 'https://parsinger.ru/4.8/7/index.html'

html = GetHtml(url=url).get_html()


class MyParser(Parser):
    def __init__(self, html):
        self.soup = html

    def _rows(self) -> list:  # get list of rows
        table = self.soup
        rows = table.find_all(name='tr')
        return rows

    def run(self):
        result = 0
        rows = self._rows()
        for row in rows:
            list_row = self._get_date_in_row(row)
            list_row = map(int, list_row)
            f_3 = lambda x: (x % 3 == 0)
            res = sum(filter(f_3, list_row))
            result += res
        return result


class Worker:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def get_tables(self):
        tables = self.soup.find(name='body'). \
            find(name='div', attrs={'class': 'tables-container'}). \
            find_all(name='table')
        return tables


def mane():
    html = GetHtml(url=url).get_html()
    tabels = Worker(html=html).get_tables()

    result = 0
    for table in tabels:
        res = MyParser(html=table).run()
        result += res

    print(result)


if __name__ == "__main__":
    mane()
