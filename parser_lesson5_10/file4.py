import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

URL = "https://parsinger.ru/draganddrop/2/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _drag_and_drop(self, browser):
        browser.implicitly_wait(10)
        actions = ActionChains(browser)

        red_square = browser.find_element(By.CSS_SELECTOR, "div#draggable")

        for square in browser.find_element(By.CSS_SELECTOR, "div#container"). \
                find_elements(By.CSS_SELECTOR, "div.box"):
            time.sleep(3)
            ic(square.get_attribute("id"))
            actions.click_and_hold(red_square).move_to_element(square)
            actions.release()

        actions.perform()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.implicitly_wait(10)
            browser.get(URL)

            self._drag_and_drop(browser=browser)

            time.sleep(5)

            return browser.find_element(By.CSS_SELECTOR, "div#message").text

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
