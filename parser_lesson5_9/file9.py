import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://parsinger.ru/selenium/5.9/7/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            checkboxs = browser.find_element(By.CSS_SELECTOR, "div#main_container").find_elements(By.CSS_SELECTOR,
                                                                                                  "div.container")
            for checkbox in tqdm(checkboxs):
                input_click = checkbox.find_element(By.TAG_NAME, "input")
                WebDriverWait(browser, 10).until(EC.element_to_be_selected(input_click))

                checkbox.find_element(By.TAG_NAME, "button").click()

            return browser.find_element(By.CSS_SELECTOR, "p#result").text

    def run(self):
        return self._parser()


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
