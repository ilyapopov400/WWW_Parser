import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from tqdm import tqdm

URL = 'https://parsinger.ru/selenium/5.8/2/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _button_click(self, browser, button):
        '''
        кликаем на кнопку, получаем значение с alert
        '''
        button.click()

        alert = browser.switch_to.alert
        result = alert.text
        alert.accept()

        return result

    def _read_to_form(self, browser, text_button):
        '''
        заносим текст с кнопки для проверки
        '''
        button_result_form = browser.find_element(By.CSS_SELECTOR, "div.res").find_element(By.ID, "input")
        button_result_form.send_keys(text_button)

        button_result_click = browser.find_element(By.CSS_SELECTOR, "div.res").find_element(By.ID, "check")
        button_result_click.click()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            buttons = browser.find_element(By.TAG_NAME, "body").find_element(By.CLASS_NAME, "main").find_elements(
                By.TAG_NAME, "input")
            for button in buttons:
                text_button = self._button_click(browser=browser, button=button)

                self._read_to_form(browser=browser, text_button=text_button)

                result = browser.find_element(By.ID, "result").text
                if result != "Неверный пин-код":
                    time.sleep(5)
                    return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
