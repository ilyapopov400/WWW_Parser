import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/selenium/5.5/5/1.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _find_forms(self, driver):
        '''
        поиск всех ячеек
        :param driver:
        :return:
        '''
        form = driver.find_element(By.CSS_SELECTOR, "body")
        form = form.find_elements(By.CSS_SELECTOR, "div#main-container[style='width: 100%;']")[0]
        forms = form.find_elements(By.XPATH, ".//div[@style]")

        return forms

    def _get_color(self, form):
        '''
        получаем цвета
        :param form:
        :return:
        '''
        color = form.find_element(By.TAG_NAME, "span")
        color = color.text

        button = form.find_element(By.TAG_NAME, "div")
        buttons = button.find_elements(By.TAG_NAME, "button")
        button = list(filter(lambda x: x.get_attribute("data-hex") == color, buttons))[0]
        button.click()

        select = form.find_element(By.CSS_SELECTOR, f"select>option[value='{color}']")
        select.click()

        checkbox = form.find_element(By.XPATH, ".//input[@type='checkbox']")
        checkbox.click()

        form_to_use = form.find_element(By.XPATH, ".//input[@type='text']")
        form_to_use.send_keys(color)

        result_button = form.find_elements(By.TAG_NAME, "button")
        result_button = list(filter(lambda x: x.text == "Проверить", result_button))[0]
        result_button.click()

    def _click_form(self, driver):
        '''
        нажимаем кнопку ОТПРАВИТЬ
        :param driver:
        :return:
        '''
        f = driver.find_element(By.XPATH, ".//button[text()='Проверить все элементы']")
        f.click()
        time.sleep(2)

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

            forms = self._find_forms(driver=driver)

            for form in forms:
                self._get_color(form=form)

            self._click_form(driver=driver)

            time.sleep(1)
            result = self._get_alert(driver=driver)
            time.sleep(5)

            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
