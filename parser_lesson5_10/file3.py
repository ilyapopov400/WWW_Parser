import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

URL = "https://parsinger.ru/selenium/5.10/2/index.html"


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

        step = browser.find_element(By.CSS_SELECTOR, "div#main_container").size.get("width")
        lines = browser.find_element(By.CSS_SELECTOR, "div#main_container"). \
            find_elements(By.TAG_NAME, "div")

        for line in lines:
            if line.get_attribute("class") == "draganddrop_end":
                break

            line_width = line.size.get("width")

            actions.drag_and_drop_by_offset(line, step - line_width, 0).perform()

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
