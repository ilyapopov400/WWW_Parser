import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://parsinger.ru/expectations/3/index.html"


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

            click_button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "btn")))
            click_button.click()
            WebDriverWait(browser, 30).until(EC.title_is("345FDG3245SFD"))
            result = browser.find_element(By.ID, "result").text

            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
