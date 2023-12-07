import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/methods/3/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _get_cookies(self, driver):
        cookies = driver.get_cookies()
        return cookies

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)
            cookies = self._get_cookies(driver=driver)
            result = sum(map(lambda x: int(x.get("value")), cookies))

            time.sleep(5)

            return result

    def run(self):
        result = self._parser()

        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
