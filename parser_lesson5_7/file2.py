import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

URL = 'https://parsinger.ru/selenium/5.7/1/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')
        self.r = set()

    def _get_alert(self, driver):
        '''
        получаем результат с всплывающего окна
        :param driver:
        :return:
        '''
        alert = driver.switch_to.alert
        alert_text = alert.text
        return alert_text

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)
            targets = driver.find_elements(By.CSS_SELECTOR, 'div > button')
            for target in tqdm(targets):
                driver.execute_script("return arguments[0].scrollIntoView(true);", target)
                time.sleep(1)
                target.click()

            result = self._get_alert(driver=driver)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
