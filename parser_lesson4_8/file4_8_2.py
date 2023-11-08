from parser_lesson4_8.file4 import GetHtml, Parser

url = 'https://parsinger.ru/table/2/index.html'

html = GetHtml(url=url).get_html()


class MyParser(Parser):

    def run(self):
        resault = 0
        rows = self._rows()[1:]
        for row in rows:
            list_row = self._get_date_in_row(row)
            try:
                res = float(list_row[0])
                resault += res
            except:
                print(list_row)
                pass
        print(resault)


def mane():
    a = MyParser(html=html)
    a.run()


if __name__ == "__main__":
    mane()
