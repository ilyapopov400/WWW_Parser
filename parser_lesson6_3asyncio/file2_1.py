import aiohttp
import asyncio
from bs4 import BeautifulSoup
from get_html import GetHtml
import time

connector = aiohttp.TCPConnector(limit=1000)
# timeout = aiohttp.ClientTimeout(total=500, connect=500, sock_connect=500, sock_read=500)

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


async def get_resalt_from_cards(link: str, session) -> int:
    '''
    получаем текст с кодом ответа с карточки
    :param link:
    :return:
    '''
    async with session.get(url=link, ssl=False) as resp:
        if resp.status == 200:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            result = int(soup.select_one("div.main").select_one("div.item_card").select_one("p.text").text)
            return result
        return 0


async def main(links):
    async with aiohttp.ClientSession() as session:
        tasks = [get_resalt_from_cards(link, session) for link in links]
        result = await asyncio.gather(*tasks)
        return result


if __name__ == '__main__':
    time1 = time.time()
    links = get_links(url=URL)
    result = sum(asyncio.run(main(links=links)))
    print(result)
    print(time.time() - time1)
# 2665626173154
# time = 3.4295742511749268
