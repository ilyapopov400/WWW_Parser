from file4 import GetHtml, Parser

url = 'https://parsinger.ru/table/3/index.html'

html = GetHtml(url=url).get_html()


class MyParser(Parser):
    def _get_date_in_row(self, row) -> list:  # get list of date in one row
        res = row.find_all(name='b')
        res = list(map(lambda x: x.text, res))
        return res

    def run(self):
        result = 0
        rows = self._rows()[1:]
        for row in rows:
            res = self._get_date_in_row(row=row)
            result += sum(map(float, res))
        print(result)



def mane():
    a = MyParser(html=html)
    a.run()


if __name__ == "__main__":
    mane()
