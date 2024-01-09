import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://parsinger.ru/selenium/5.9/2/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

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
            locator = (By.ID, "qQm9y1rk")
            target = EC.presence_of_element_located(locator)
            element = WebDriverWait(browser, 1000).until(target)
            element.click()

            result = self._get_alert(browser=browser)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
