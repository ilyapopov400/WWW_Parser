import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/methods/1/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def run(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)
            while True:
                try:
                    form = driver.find_element(By.ID, "result")
                    ic(form.text)
                    result = int(form.text)
                    time.sleep(3)
                    return result
                except ValueError:
                    driver.refresh()
                    # time.sleep(1)


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
