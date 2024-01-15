import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm
import re

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webcolors import rgb_to_name

URL = "https://parsinger.ru/selenium/5.10/8/index.html"


class Parser:

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def drag_and_drop(self, browser):
        for element in tqdm(browser.find_element(By.XPATH, "//div[@id='pieces_container']"). \
                                    find_elements(By.XPATH, "div")):
            step = int(re.search(r'\d+', element.get_attribute("id")).group(0))
            ic(step)
            ActionChains(browser).click_and_hold(element).move_by_offset(step, 0).release().perform()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.implicitly_wait(10)
            browser.get(URL)

            self.drag_and_drop(browser=browser)

            time.sleep(1)
            return browser.find_element(By.XPATH, "//p[@id='message']").text

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
