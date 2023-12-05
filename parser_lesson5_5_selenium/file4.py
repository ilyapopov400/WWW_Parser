import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/selenium/5.5/3/1.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _find_form(self, driver):
        '''
        поиск всех контейнеров
        :param driver:
        :return:
        '''
        form = driver.find_element(By.ID, "container")
        forms = form.find_elements(By.CLASS_NAME, "parent")
        return forms

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)

            forms = self._find_form(driver=driver)
            f = lambda x: x.find_element(By.CLASS_NAME, "checkbox").is_selected() is True
            forms_filter = filter(f, forms)

            result = sum(map(lambda x: int(x.text), forms_filter))

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
