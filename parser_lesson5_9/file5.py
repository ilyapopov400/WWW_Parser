import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://parsinger.ru/selenium/5.9/3/index.html"


class Parser:
    ids_to_find = ['xhkVEkgm', 'QCg2vOX7', '8KvuO5ja', 'CFoCZ3Ze', '8CiPCnNB', 'XuEMunrz', 'vmlzQ3gH', 'axhUiw2I',
                   'jolHZqD1', 'ZM6Ms3tw', '25a2X14r', 'aOSMX9tb', 'YySk7Ze3', 'QQK13iyY', 'j7kD7uIR']

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _get_alert(self, browser):
        '''
        получаем результат с всплывающего окна
        :param driver:
        :return:
        '''
        alert = browser.switch_to.alert
        alert_text = alert.text
        return alert_text

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            while bool(self.ids_to_find):
                try:
                    id = random.choice(self.ids_to_find)

                    locator = (By.ID, id)
                    target = EC.visibility_of_element_located(locator)
                    element = WebDriverWait(browser, .01).until(target)
                    element.click()
                    self.ids_to_find.remove(id)
                except TimeoutException:
                    pass

            result = self._get_alert(browser=browser)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
