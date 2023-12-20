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


class ParserOnePage:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _get_text(self, browser):
        window = browser.find_element(By.TAG_NAME, "html").text

        ic(window)


    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(self.url)
            result = 0

            self._get_text(browser=browser)

            time.sleep(3)

            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = ParserOnePage(url=URL).run()
    ic(result)
