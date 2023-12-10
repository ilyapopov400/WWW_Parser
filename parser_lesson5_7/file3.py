import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

URL = 'https://parsinger.ru/selenium/5.7/5/index.html'


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
        actions = ActionChains(browser)
        for form in browser.find_elements(By.TAG_NAME, "button"):
            value = float(form.text)
            actions.click_and_hold(form).pause(value).release(form).perform()
            time.sleep(.5)

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)

            self._put_buttons(browser=browser)
            time.sleep(3)

            result = self._get_alert(browser=browser)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
