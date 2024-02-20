import time
import aiofiles
import asyncio
import aiohttp
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from icecream import ic

URL = "https://parsinger.ru/asyncio/aiofile/2/index.html"


class Parser:
    def __init__(self, url):
        self.url = url

    def _fake_user_agent(self):  # crate fake user agent
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        return fake_ua

    def _links_of_page(self):  # получили список ссылок на СТРАНИЦЫ с картинками
        header = self._fake_user_agent()
        response = requests.get(url=self.url, headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select_one("div.item_card").select("a")
        links = map(lambda x: x.get("href"), links)
        links = map(lambda x: "https://parsinger.ru/asyncio/aiofile/2/{}".format(x), links)
        return links

    async def _get_cards(self, link: str, session) -> list:  # получаем список ссылок изображений карточек
        async with session.get(url=link, ssl=False) as resp:
            soup = BeautifulSoup(await resp.text(), 'lxml')

            cards = soup.select_one("div.main").select_one("div.item_card")
            cards = cards.select("div.item")

            cards = map(lambda x: x.select_one("div.img_box"), cards)
            cards = map(lambda x: x.select_one("img.picture"), cards)
            cards = map(lambda x: x.get("src"), cards)
        return list(cards)

    async def _links_of_image(self):
        """
        Асинхронно собираем все ссылки на картинки(карточки)
        :return: список ссылок на картинки
        """
        links = self._links_of_page()
        cards = list()
        async with aiohttp.ClientSession() as session:
            tasks = [self._get_cards(link, session) for link in links]
            cards.extend(await asyncio.gather(*tasks))
        result = set()
        for card in cards:
            for image in card:
                result.add(image)
        return result

    def __call__(self, *args, **kwargs):
        links_of_images = asyncio.run(self._links_of_image())  # список ссылок на картинки
        result = links_of_images
        return result


if __name__ == "__main__":
    result = Parser(url=URL)()
    print(result)
