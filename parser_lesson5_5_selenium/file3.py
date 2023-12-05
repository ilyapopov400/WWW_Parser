import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/selenium/5.5/2/1.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _find_form(self, driver):
        '''
        поиск всех ячеек
        :param driver:
        :return:
        '''
        form = driver.find_element(By.CSS_SELECTOR, "body")
        form = form.find_element(By.CLASS_NAME, "container")
        form = form.find_element(By.ID, "textfields-container")
        forms = form.find_elements(By.CLASS_NAME, "text-field")
        return forms

    def _click_form(self, driver):
        '''
        нажимаем кнопку ОТПРАВИТЬ
        :param driver:
        :return:
        '''
        form = driver.find_element(By.ID, "checkButton")
        form.click()

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

            forms = self._find_form(driver=driver)
            forms_filter = filter(lambda x: x.is_enabled() is True, forms)
            [form.clear() for form in forms_filter]

            self._click_form(driver=driver)

            result = self._get_alert(driver=driver)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
