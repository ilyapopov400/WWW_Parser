import time
from bs4 import BeautifulSoup
from get_html import GetHtml

URL = "https://parsinger.ru/asyncio/create_soup/1/index.html"


def get_links(url):
    '''
    собираем в список все ссылки, на которые необходимо перейти
    :param url:
    :return:
    '''
    html = GetHtml(url=url).get_html()
    soup = BeautifulSoup(html, 'lxml')
    links = map(
        lambda x: x.get("href"),
        soup.select_one("body").select_one("div.main").select_one("div.item_card").select("a.lnk_img")
    )
    links = map(lambda x: "https://parsinger.ru/asyncio/create_soup/1/{}".format(x), links)
    return links


def get_resalt_from_cards(link):
    '''
    получаем текст с кодом ответа с карточки
    :param link:
    :return:
    '''
    html = GetHtml(url=link).get_html()
    soup = BeautifulSoup(html, 'lxml')
    result = int(soup.select_one("div.main").select_one("div.item_card").select_one("p.text").text)
    return result


if __name__ == '__main__':
    time1 = time.time()
    links = get_links(url=URL)
    result = list()
    for link in links:
        try:
            res = get_resalt_from_cards(link=link)
            result.append(res)
            print(res)
        except:
            pass
    print(sum(result))
    print(time.time() - time1)

# 2665626173154
# time = 128.14284801483154
