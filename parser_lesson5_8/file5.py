import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm

URL = 'https://parsinger.ru/window_size/1/'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _screen_installation(self, browser):
        browser.set_window_size(width=555, height=555 + 129)
        ic(browser.get_window_size().get('height'))
        ic(browser.get_window_size().get('width'))
        time.sleep(3)

    def _get_result(self, browser):
        result = browser.find_element(By.ID, "result").text
        return result

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            self._screen_installation(browser=browser)
            result = self._get_result(browser=browser)
            time.sleep(5)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
