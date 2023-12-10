import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

URL = 'https://parsinger.ru/scroll/2/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _get_alert(self, browser):
        '''
        получаем результат с всплывающего окна
        :param driver:
        :return:
        '''
        alert = browser.switch_to.alert
        alert_text = alert.text
        return alert_text

    def _put_buttons(self, browser):
        span_sum = 0
        for form in tqdm(browser.find_elements(By.XPATH, ".//div[@class='item']")):
            button = form.find_element(By.XPATH, ".//input[@type='checkbox']")
            button.click()
            span = form.find_element(By.XPATH, ".//span").text
            if bool(span):
                span_sum += int(span)
        return span_sum

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            result = self._put_buttons(browser=browser)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
