import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm

URL = 'https://parsinger.ru/selenium/5.8/5/index.html'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _work_in_iframe(self, browser, iframe):
        browser.switch_to.frame(iframe)
        browser.find_element(By.TAG_NAME, "body").find_element(By.TAG_NAME, "button").click()
        text = browser.find_element(By.ID, "numberDisplay").text
        browser.switch_to.default_content()
        return text

    def _take_result(self, browser):
        result = list()
        window = browser.find_element(By.ID, "main_container")
        iframes = window.find_elements(By.TAG_NAME, "iframe")
        for iframe in tqdm(iframes):
            number = int(self._work_in_iframe(browser=browser, iframe=iframe))
            result.append(number)

        return result

    def _checking_the_result(self, browser, list_number):
        for number in tqdm(list_number):
            target = browser.find_element(By.TAG_NAME, "body").find_element(By.CSS_SELECTOR, "div.main")
            button = target.find_element(By.TAG_NAME, "input")
            button.send_keys(number)
            target.find_element(By.ID, "checkBtn").click()
            try:
                alert = browser.switch_to.alert
                alert_text = alert.text
                alert.accept()
                return alert_text
            except NoAlertPresentException:
                pass
            button.clear()
            time.sleep(1)

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            number_from_frame = self._take_result(browser=browser)
            result = self._checking_the_result(browser=browser, list_number=number_from_frame)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
