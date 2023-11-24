import get_html
import json
from icecream import ic


class CreateDict:
    def __init__(self, js: list):
        self.js = js
        self.result = dict()

    def _create_dict(self):
        for dict_js in self.js:
            categories = dict_js.get("categories")

            val = self.result.get(categories, 0)
            count = int(dict_js.get("article"))
            price = int(dict_js.get('description').get("rating"))
            self.result[categories] = val + count * price

    def run(self):
        self._create_dict()
        return self.result


def mane():
    url = 'https://parsinger.ru/4.6/1/res.json'
    html = get_html.GetHtml(url=url).get_html()

    js = json.loads(html)

    result = CreateDict(js=js).run()

    ic(result)


if __name__ == "__main__":
    mane()
