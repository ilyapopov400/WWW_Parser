import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://parsinger.ru/selenium/5.9/5/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _touch(self, browser):
        locator = By.CSS_SELECTOR, "div#ad_window"
        target = EC.invisibility_of_element_located(locator)
        WebDriverWait(browser, 10).until(target)

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            result = list()
            browser.get(URL)

            windows = browser.find_element(By.ID, "main_container").find_elements(By.CSS_SELECTOR, "div.box_button")
            for window in windows:
                ic(window.get_attribute("data-index"))
                window.click()

                browser.find_element(By.CSS_SELECTOR, "button#close_ad").click()
                self._touch(browser=browser)
                time.sleep(5)

                ic(window.text)
                result.append(window.text)
                ic(result)
            return "-".join(result)

    def run(self):
        return self._parser()


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
