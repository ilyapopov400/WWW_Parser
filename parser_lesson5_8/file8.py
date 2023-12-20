import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm
from itertools import product

URL = "https://parsinger.ru/blank/3/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            result = 0
            buttons = browser.find_element(By.TAG_NAME, "body").find_element(By.CSS_SELECTOR, "div.main").find_elements(
                By.TAG_NAME, "input")
            for button in buttons:
                button.click()
            for window in browser.window_handles:
                browser.switch_to.window(window)
                title = browser.title
                try:
                    result += int(title)
                except ValueError:
                    pass

            time.sleep(3)

            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
