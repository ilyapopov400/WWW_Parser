import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm
import json
import os

URL = 'https://parsinger.ru/scroll/4/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')
        self.r = set()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)
            result = 0
            elements = driver.find_elements(By.CLASS_NAME, 'btn')

            for element in tqdm(elements):
                driver.execute_script("return arguments[0].scrollIntoView(true);",
                                      element)  # скролим до элемента element
                element.click()
                result += int(driver.find_element(By.ID, 'result').text)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
