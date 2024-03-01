import time
import aiofiles
import asyncio
import aiohttp
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from icecream import ic
import os
import shutil

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

    async def _write_file(self, session, url, name_img):
        """
        записываем файл в папку images
        :param session:
        :param url:
        :param name_img:
        :return:
        """
        async with aiofiles.open(f'images/{name_img}', mode='wb') as f:
            async with session.get(url, ssl=False) as response:
                async for x in response.content.iter_chunked(1024):
                    await f.write(x)
            ic(f'Изображение сохранено {name_img}')

    async def _creater_images(self, img_url):
        """
        Записываем изображения в асинхроном режиме
        :param img_url:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            tasks = list()
            for link in img_url:
                name_img = link.split("/")[-1]
                task = asyncio.create_task(self._write_file(session, link, name_img))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def _get_folder_size(self, filepath, size=0):
        """
        получаем вес папки images
        :param filepath:
        :param size:
        :return:
        """
        for root, dirs, files in os.walk(filepath):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
        return size

    def __call__(self, *args, **kwargs):
        if os.path.exists('images'):
            shutil.rmtree(path='images')
        else:
            os.makedirs('images', exist_ok=True)
        links_of_images = asyncio.run(self._links_of_image())  # список ссылок на картинки
        asyncio.run(self._creater_images(img_url=links_of_images))

        result = self._get_folder_size(filepath="images")
        return result


if __name__ == "__main__":
    time_now = time.time()
    result = Parser(url=URL)()
    print(result)
    print("Затрачено времени: {} секунд".format(round(time.time() - time_now)))

# 212788721
# Затрачено времени: 24 секунд
