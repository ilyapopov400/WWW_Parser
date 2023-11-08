from parserlesson4_9.file4 import GetHtml, Parser

url = 'https://parsinger.ru/table/5/index.html'

html = GetHtml(url=url).get_html()


class MyParser(Parser):
    def _get_date_in_row(self, row) -> list:  # get list of date in one row
        res1 = row.find(name='td', attrs={'class': 'orange'})
        res2 = row.find_all(name='td')[-1]
        res = list(map(lambda x: float(x.text), (res1, res2)))
        return res

    def run(self):
        result = 0
        rows = self._rows()[1:]
        for row in rows:
            res = self._get_date_in_row(row=row)
            result += res[0] * res[1]

        print(result)


def mane():
    MyParser(html=html).run()


if __name__ == "__main__":
    mane()
