import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm
from itertools import product

URL = 'https://parsinger.ru/window_size/2/index.html'


class Parser:
    window_size_x = [616, 648, 680, 701, 730, 750, 805, 820, 855, 890, 955, 1000]
    window_size_y = [300, 330, 340, 388, 400, 421, 474, 505, 557, 600, 653, 1000]

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _screen_installation(self, browser, width, height):
        browser.set_window_size(width=width, height=height + 129)

    def _get_result(self, browser):
        result = browser.find_element(By.ID, "result").text
        return result

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            for (width, height) in product(self.window_size_x, self.window_size_y):
                self._screen_installation(browser=browser, width=width, height=height)
                if result := self._get_result(browser=browser):
                    time.sleep(5)
                    return result
            time.sleep(5)
            return

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
