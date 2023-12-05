import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/selenium/5.5/4/1.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _find_form(self, driver):
        '''
        поиск всех ячеек
        :param driver:
        :return:
        '''
        form = driver.find_element(By.CSS_SELECTOR, "body")
        form = form.find_element(By.ID, "container")
        forms = form.find_elements(By.CLASS_NAME, "parent")
        return forms

    def _pass_date(self, form):
        element = form.find_element(By.XPATH, ".//textarea[@color='gray']")
        text = element.text
        element.clear()

        element = form.find_element(By.XPATH, ".//textarea[@color='blue']")
        element.send_keys(text)

        element = form.find_element(By.XPATH, ".//button")
        element.click()

    def _click_form(self, driver):
        '''
        нажимаем кнопку ОТПРАВИТЬ
        :param driver:
        :return:
        '''
        form = driver.find_element(By.ID, "checkAll")
        form.click()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)

            forms = self._find_form(driver=driver)

            for form in forms:
                self._pass_date(form=form)

            self._click_form(driver=driver)

            form = driver.find_element(By.ID, "congrats")

            result = form.text
            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
