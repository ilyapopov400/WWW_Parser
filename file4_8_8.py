from bs4 import BeautifulSoup

from file4 import GetHtml

url = 'https://parsinger.ru/4.8/8/index.html'


class MyParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def table(self):
        table = self.soup.select_one('body'). \
            find(name='table', attrs={'id': 'mainTable'}). \
            select_one('tr').find(name='td', attrs={'colspan': '3'}).select_one('table')
        return table

    # def run(self):  # TODO
    #     table = self.table()
    #     result = table.find_all(name=['td', 'th'])
    #     result = list(filter(lambda x: x.get('colspan'), result))
    #     summa = 0
    #     for i in result:
    #         print(i)
    #         summa += int(i.text)
    #     print(len(list(result)))
    #     print(summa)

    def run(self):  # TODO
        table = self.table()
        result = table.find_all(lambda tag: tag.has_attr('colspan'))
        print(*result, sep='\n********\n')
        result = sum(map(lambda x: int(x.text), result))
        print(result)


def mane():
    html = GetHtml(url=url).get_html()
    a = MyParser(html=html)
    a.run()


if __name__ == "__main__":
    mane()
