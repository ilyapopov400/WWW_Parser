import get_html
import json
from icecream import ic


def mane():
    url = 'https://parsinger.ru/downloads/get_json/res.json'
    html = get_html.GetHtml(url=url).get_html()

    js = json.loads(html)
    result = dict()

    for dict_js in js:
        categories = dict_js.get("categories")

        val = result.get(categories, 0)
        result[categories] = val + int(dict_js.get("count"))

    ic(result)


if __name__ == "__main__":
    mane()
