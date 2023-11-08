from parserlesson4_9.file4 import GetHtml, Parser

url = 'https://parsinger.ru/table/4/index.html'

html = GetHtml(url=url).get_html()


class MyParser(Parser):
    def _get_date_in_row(self, row) -> list:  # get list of date in one row
        res = row.find_all(name='td', attrs={'class': 'green'})
        res = list(map(lambda x: x.text, res))
        return res

    def run(self):
        result = 0
        rows = self._rows()[1:]
        for row in rows:
            list_row = self._get_date_in_row(row)
            res = sum(map(float, list_row))
            result += res
        print(result)


def mane():
    MyParser(html=html).run()


if __name__ == "__main__":
    mane()
