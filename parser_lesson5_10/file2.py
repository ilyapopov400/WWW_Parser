import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

URL = "https://parsinger.ru/draganddrop/3/index.html"


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

        element = browser.find_element(By.CSS_SELECTOR, "div#block1")
        x_element = element.location.get("x")

        targets = browser.find_elements(By.CSS_SELECTOR, "div.controlPoint")
        x_target = max(targets, key=lambda x: x.location.get("x")).location.get("x")
        ic(x_target - x_element)

        for x in range(1, (x_target - x_element)):
            ic(x)
            actions.click_and_hold(element).move_by_offset(1, 0)
        actions.release().perform()

        actions.click_and_hold(element).move_by_offset(100, 100).release().perform()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.implicitly_wait(10)
            browser.get(URL)

            self._drag_and_drop(browser=browser)

            time.sleep(5)

            return browser.find_element(By.CSS_SELECTOR, "p#message").text

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
