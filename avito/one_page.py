import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm
from itertools import product
from selenium.common.exceptions import NoSuchElementException

URL = 'https://www.avito.ru/volgograd/kollektsionirovanie/lp_deep_purple_24_carat_purple_japan_1985_mint_3567795461'
# URL = "https://www.avito.ru/volgograd/kollektsionirovanie/lp_deep_purple_24_carat_purple_japan_1985_mint_3567795461"

class ParserOnePage:
    '''
    парсинг одной страницы avito
    :return текст описания товара
    '''

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _target_text(self, browser) -> list:
        target_text = list()
        window = browser.find_element(By.CSS_SELECTOR, "div.style-item-description-html-qCwUL")
        for line in window.find_elements(By.TAG_NAME, "p"):
            target_text.append(line.text)
        return target_text

    def _parser(self) -> str:
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(self.url)

            result = self._target_text(browser=browser)

            return ", ".join(result)

    def run(self) -> str:
        result = self._parser()
        return result


if __name__ == "__main__":
    result = ParserOnePage(url=URL).run()
    ic(result)
