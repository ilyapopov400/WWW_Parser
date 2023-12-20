import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm
from itertools import product
import math

URL = "https://parsinger.ru/blank/3/index.html"


class Parser:
    sites = ['http://parsinger.ru/blank/1/1.html', 'http://parsinger.ru/blank/1/2.html',
             'http://parsinger.ru/blank/1/3.html',
             'http://parsinger.ru/blank/1/4.html', 'http://parsinger.ru/blank/1/5.html',
             'http://parsinger.ru/blank/1/6.html', ]

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _get_number(self, browser):
        button = browser.find_element(By.TAG_NAME, "body").find_element(By.CSS_SELECTOR, "div.main")
        button.find_element(By.CSS_SELECTOR, "div.check_box"). \
            find_element(By.CSS_SELECTOR, "input.checkbox_class").click()
        time.sleep(1)
        number = float(browser.find_element(By.ID, "result").text)
        return number

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            result = 0
            for site in self.sites:
                browser.get(url=site)
                result += math.sqrt(self._get_number(browser))
            return round(result, 9)

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
