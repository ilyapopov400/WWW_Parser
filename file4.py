import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://parsinger.ru/table/1/index.html'


class GetHtml:
    '''
    получаем html в виде строки с использованием UserAgent
    '''

    def __init__(self, url):
        self.url = url

    def _fake_user_agent(self):  # crate fake user agent
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        return fake_ua

    def get_html(self) -> str:
        header = self._fake_user_agent()
        response = requests.get(url=self.url, headers=header)
        response.encoding = 'utf-8'
        if response:
            print(response.status_code)
            return response.text
        return 'ERROR {}'.format(response.status_code)


html = GetHtml(url=url).get_html()


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def _rows(self) -> list:  # get list of rows
        table = self.soup.select_one('body').select_one('div.main').select_one('table')
        rows = table.find_all(name='tr')
        return rows

    def _get_date_in_row(self, row) -> list:  # get list of date in one row
        res = row.find_all(name='td')
        res = list(map(lambda x: x.text, res))
        return res

    def run(self):
        result = set()
        rows = self._rows()[1:]
        for row in rows:
            list_row = self._get_date_in_row(row)
            try:
                res = set(map(float, list_row))
                result.update(res)
            except:
                print('??????')
                pass
        print(sum(result))


def mane():
    Parser(html=html).run()


if __name__ == "__main__":
    mane()
