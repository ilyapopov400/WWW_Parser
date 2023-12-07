import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

URL = 'https://parsinger.ru/methods/5/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')
        self.result = dict()

    def _get_cookies(self, driver):
        cookies = driver.get_cookies()
        return cookies

    def _list_pages(self, driver):
        list_pages = driver.find_element(By.TAG_NAME, "body")
        list_pages = list_pages.find_element(By.CLASS_NAME, "main")
        list_pages = list_pages.find_elements(By.CLASS_NAME, "urls")
        return list_pages

    def _click_one_page(self, driver, list_pages):
        for form in list_pages:
            button_click = form.find_element(By.TAG_NAME, "a")
            button_click.click()

            coocies = self._get_cookies(driver=driver)

            expiry = coocies[0].get("expiry")
            text = driver.find_element(By.ID, "result").text
            self.result[text] = expiry

            driver.back()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as driver:
            driver.get(URL)

            list_pages = self._list_pages(driver=driver)
            self._click_one_page(driver=driver, list_pages=list_pages)

            result = self.result
            result = max(result, key=result.get)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()

        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
