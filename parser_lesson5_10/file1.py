import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

URL = "https://parsinger.ru/draganddrop/1/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _drag_and_drop(self, browser):
        element = browser.find_element(By.CSS_SELECTOR, "div#draggable")
        movie_to_element = browser.find_element(By.CSS_SELECTOR, "div#field2")
        time.sleep(5)

        actions = ActionChains(browser)

        actions.click_and_hold(element).move_to_element(movie_to_element).perform()
        time.sleep(5)

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.implicitly_wait(10)
            browser.get(URL)

            while bool(result := browser.find_element(By.CSS_SELECTOR, "div#result").text) is False:
                self._drag_and_drop(browser=browser)
                ic(result)

            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
