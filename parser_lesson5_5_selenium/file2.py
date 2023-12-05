import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/selenium/5.5/1/1.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)

            form = driver.find_element(By.CSS_SELECTOR, "body")
            form = form.find_element(By.CLASS_NAME, "container")
            form = form.find_element(By.ID, "textfields-container")
            forms = form.find_elements(By.CLASS_NAME, "text-field")
            [el.clear() for el in forms]

            form = driver.find_element(By.CSS_SELECTOR, "body")
            form = form.find_element(By.CLASS_NAME, "container")
            form = form.find_element(By.ID, "checkButton")
            form.click()

            alert = driver.switch_to.alert
            alert_text = alert.text

            time.sleep(3)
            return alert_text

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
