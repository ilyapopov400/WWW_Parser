import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webcolors import rgb_to_name

URL = "https://parsinger.ru/selenium/5.10/4/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def drag_and_drop(self, browser):
        ls_bools = list()
        for bool in tqdm(
                browser.find_element(By.CSS_SELECTOR, "div.basket_with_toys").find_elements(By.TAG_NAME, "div")):
            ls_bools.append(bool)
            bool_color = bool.get_attribute("class").split()[1].split("_")[0]
            for square in browser.find_element(By.CSS_SELECTOR, "div.main_container") \
                    .find_elements(By.XPATH, "./div"):
                if square.get_attribute("class") == "basket_with_toys":
                    pass
                else:
                    if bool_color in square.get_attribute("class"):
                        actions = ActionChains(browser)
                        actions.drag_and_drop(bool, square).perform()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.implicitly_wait(10)
            browser.get(URL)

            self.drag_and_drop(browser=browser)

            time.sleep(1)
            return browser.find_element(By.CSS_SELECTOR, "p.message").text

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
