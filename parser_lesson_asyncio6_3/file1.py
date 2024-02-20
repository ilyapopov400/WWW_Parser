import aiohttp
import asyncio
from bs4 import BeautifulSoup


def get_links() -> list:
    links = ["https://parsinger.ru/html/index{}_page_{}.html".format(i, j) for i in range(1, 6) for j in range(1, 5)]
    return links


async def get_cards(link: str, session) -> list:
    async with session.get(url=link, ssl=False) as resp:
        soup = BeautifulSoup(await resp.text(), 'lxml')
        cards = soup.find_all("div", class_="sale_button")
        cards = [card.find("a").get("href") for card in cards]
        cards = ["https://parsinger.ru/html/{}".format(card) for card in cards]

    return cards


async def calculation(card: str, session) -> float:
    async with session.get(url=card, ssl=False) as resp:
        soup = BeautifulSoup(await resp.text(), 'lxml')
        price = int(soup.find("span", id="price").text.split()[0])
        old_price = int(soup.find("span", id="old_price").text.split()[0])
        count = int(soup.find("span", id="in_stock").text.split()[-1])
        return (old_price - price) * count


async def main1():
    links = get_links()
    cards = list()
    async with aiohttp.ClientSession() as session:
        tasks = [get_cards(link, session) for link in links]
        cards.extend(await asyncio.gather(*tasks))
    return cards


async def main2(links):
    cards = list()
    async with aiohttp.ClientSession() as session:
        tasks = [calculation(link, session) for link in links]
        cards.append(await asyncio.gather(*tasks))
    return cards


if __name__ == '__main__':
    result_cards = list()
    cards = asyncio.run(main1())
    for card in cards:
        for i in card:
            result_cards.append(i)

    result = asyncio.run(main2(links=result_cards))[0]
    print(sum(result))
