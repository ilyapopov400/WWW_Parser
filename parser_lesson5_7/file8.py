import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from tqdm import tqdm

URL = 'https://parsinger.ru/selenium/5.7/4/index.html'


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
        # alert.click()
        alert_text = alert.text
        return alert_text

    def _put_button(self, element):
        elements = element.find_elements(By.TAG_NAME, "input")
        for number, button in enumerate(elements):
            value = int(button.get_attribute("value"))
            if value % 2 == 0:
                button.click()
            if number == (len(elements) - 1):
                button.send_keys(Keys.DOWN)
                time.sleep(.2)

    def _put_to_file(self, brouser):
        '''
        записываем в файл brouser
        '''
        html = brouser.page_source
        with open('temp_file8.html', 'w') as file:
            file.write(html)

    def _scroll(self, window):
        '''
        скролим внутри окна window, используя browser
        '''
        flag1 = True
        step = 1  # количество итераций для самоконтроля
        while flag1:
            el = window.find_element(By.CLASS_NAME, "child_container")
            self._put_button(element=el)
            ic(step)

            while True:
                try:
                    patch = "./following-sibling::*[1]"
                    el = el.find_element(By.XPATH, patch)
                    self._put_button(element=el)

                    step += 1
                    ic(step)


                except Exception as exx:
                    ic(exx)
                    break
            flag1 = False
        return

    def _get_windows(self, browser) -> list:
        '''
        получаем список окон для дальнейшей прокрутки
        :param browser:
        :return:
        '''
        windows = browser.find_element(By.TAG_NAME, "body"). \
            find_elements(By.ID, "main_container")
        return windows

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            ic(browser.execute_script("return document.documentURI;"))

            windows = self._get_windows(browser=browser)

            for window in windows:
                self._scroll(window=window)

            time.sleep(5)

            button = windows[0].find_element(By.CSS_SELECTOR, "button.alert_button")
            button.click()
            time.sleep(5)
            result = self._get_alert(browser=browser)
            time.sleep(10)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
