import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from tqdm import tqdm

URL = 'https://parsinger.ru/selenium/5.8/1/index.html'


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
            buttons = browser.find_element(By.TAG_NAME, "body").find_element(By.CLASS_NAME, "main").find_elements(
                By.TAG_NAME, "input")
            for button in buttons:
                button.click()
                alert = browser.switch_to.alert
                ic(alert.text)
                alert.accept()
                result = browser.find_element(By.ID, "result").text
                if bool(result):
                    return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
