from parser_lesson4_8.file4 import GetHtml, Parser

url = 'https://parsinger.ru/table/5/index.html'

html = GetHtml(url=url).get_html()


class MyParser(Parser):
    def run(self):
        result = dict()
        rows = self._rows()[1:]
        for row in rows:
            list_row = self._get_date_in_row(row)
            for e, num in enumerate(list_row):
                key = '{} column'.format(e+1)
                val = result.get(key, 0)
                result[key] = round((val + float(num)), 3)
        print(result)


def mane():
    MyParser(html=html).run()


if __name__ == "__main__":
    mane()
