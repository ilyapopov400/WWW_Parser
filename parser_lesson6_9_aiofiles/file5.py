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

URL = "https://parsinger.ru/asyncio/aiofile/3/index.html"


class ParserLinksAsynchronous:
    """
    по списку ссылок асинхронно ходит по страницам и собирает следующие ссылки
    """

    def __init__(self, links: list, parsing_page, prefix=None):
        """

        :param links: список ссылок для парсинга
        :param prefix: префикс к ссылке
        :param parsing_page: функция получения ссылки с страницы
        """
        self.links = links
        self.prefix = prefix
        self.parsing_page = parsing_page

    async def _get_cards(self, link: str, session) -> list:  # получаем список ссылок c вложенных страниц (2-й уровень)
        async with session.get(url=link, ssl=False) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            links = self.parsing_page(soup=soup, prefix=self.prefix)
        return links

    async def _links_of_image(self):
        """
        Асинхронно собираем все ссылки на картинки(карточки)
        :return: список ссылок на картинки
        """
        links = self.links
        cards = list()
        conn = aiohttp.TCPConnector(limit=5)  # TODO важно установить!
        async with aiohttp.ClientSession(connector=conn) as session:
            tasks = [self._get_cards(link, session) for link in links]
            cards.extend(await asyncio.gather(*tasks))
        result = list()
        for card in cards:
            for image in card:
                result.append(image)
        return result

    def __call__(self, *args, **kwargs):
        links_of_images = asyncio.run(self._links_of_image())  # список ссылок страницы с картинками
        return links_of_images


class ParserLinksImages:
    """
    Получаем ссылки на картинки в виде списка при вызове экземпляра класса
    """

    def __init__(self, url):
        self.url = url
        self.first_level_prefix = "https://parsinger.ru/asyncio/aiofile/3/"
        self.second_level_prefix = "https://parsinger.ru/asyncio/aiofile/3/depth2/"
        self.parser = ParserLinksAsynchronous

    @staticmethod
    def _fake_user_agent():  # crate fake user agent
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        return fake_ua

    @staticmethod
    def _parsing_of_one_page(soup, prefix) -> list:
        """
        Парсим одну страницу с картинками
        получаем список ссылок со страницы
        второй уровень вложенности
        :return:
        """
        cards = soup.select_one("div.main").select_one("div.item_card").select("a")
        cards = map(lambda x: x.get("href"), cards)
        cards = map(lambda x: "{}{}".format(prefix, x), cards)
        return list(cards)

    @staticmethod
    def _parsing_of_two_page(soup, prefix) -> list:
        """
        Парсим одну страницу с картинками
        получаем список ссылок со страницы
        второй уровень вложенности
        :return:
        """
        try:
            cards = soup.select_one("body").select_one("div.main").select_one("div.item_card").select("div.item")
            cards = map(lambda x: x.select_one("div.img_box"), cards)
            cards = map(lambda x: x.select_one("img.picture"), cards)
            cards = map(lambda x: x.get("src"), cards)
            return list(cards)
        except:
            ic(soup)
            return [False, ]

    def _links_of_base_page(self):  # получили список ссылок на ОСНОВНОЙ странице
        header = self._fake_user_agent()
        response = requests.get(url=self.url, headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select_one("div.main").select_one("div.item_card").select("a")
        links = map(lambda x: x.get("href"), links)
        links = map(lambda x: "{}{}".format(self.first_level_prefix, x), links)
        return list(links)

    def __call__(self, *args, **kwargs):
        links_one = self._links_of_base_page()
        links_two = self.parser(links=links_one, prefix=self.second_level_prefix,
                                parsing_page=self._parsing_of_one_page)()
        result_images = set()
        res = self.parser(links=links_two, parsing_page=self._parsing_of_two_page)()
        for img in res:
            if img:
                result_images.add(img)
        return result_images


class SaveImages:
    """
    При вызове экземпляра класса, скачиваются картинки по links
    сохраняются в директорию path
    """
    def __init__(self, links, path):
        self.path = path
        self.links = links

    async def _write_file(self, session, url, name_img):
        """
        записываем файл в папку images
        :param session:
        :param url:
        :param name_img:
        :return:
        """
        async with aiofiles.open(f'{self.path}/{name_img}', mode='wb') as f:
            async with session.get(url, ssl=False) as response:
                async for x in response.content.iter_chunked(1024):
                    await f.write(x)
            # ic(f'Изображение сохранено {name_img}')

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

    def __call__(self, *args, **kwargs):
        asyncio.run(self._creater_images(img_url=self.links))


class Parser:
    def __init__(self, url, path_directory):
        self.url = url
        self.path_directory = path_directory
        self.links_of_images = ParserLinksImages(url=url)()
        self.save_images = SaveImages

    @staticmethod
    def _get_folder_size(filepath, size=0):
        """
        получаем размер всех файлов в папке filepath в bytes
        :param filepath:
        :param size:
        :return:
        """
        for root, dirs, files in os.walk(filepath):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
        return size

    @staticmethod
    def _create_directory(path) -> None:
        """
        удаляем содержимое с директории path, если она есть и создаем ее заново
        :param path:
        :return: None
        """
        if os.path.exists(path):
            shutil.rmtree(path=path)
        os.makedirs(path, exist_ok=True)

    def __call__(self, *args, **kwargs):
        self._create_directory(path=self.path_directory)
        ic("Скачано {} изображений".format(len(self.links_of_images)))
        self.save_images(links=self.links_of_images, path=self.path_directory)()

        return "{} байт".format(self._get_folder_size(filepath=self.path_directory))


if __name__ == "__main__":
    time_now = time.time()
    result = Parser(url=URL, path_directory="images")()
    print(result)
    print("Затрачено времени: {} секунд".format(round(time.time() - time_now)))

    # links_of_page = ParserLinksImages(url=URL)()  # 100 ссылок
    # a = ParserLinks(links=links_of_page)()
    # print(len(a))

    # print(links_of_page, len(links_of_page))
