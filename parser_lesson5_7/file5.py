import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

URL = 'https://parsinger.ru/infiniti_scroll_1/'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        self.options_chrome.add_argument('--headless')

    def _get_sum(self, browser):
        span_sum = dict()
        flag = True

        while flag:
            while not bool(targets := browser.find_element(By.ID, "scroll-container").
                    find_elements(By.TAG_NAME, "span")):
                pass
            else:
                for el in tqdm(targets):
                    click = el.find_element(By.TAG_NAME, "input")
                    click.click()
                    span_sum[el.get_attribute('id')] = int(el.text)
                    browser.execute_script("return arguments[0].scrollIntoView(true);", click)
                    stop = el.get_attribute('class')
                    if stop == "last-of-list":
                        flag = False

        return span_sum

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            result = self._get_sum(browser=browser)
            result = sum(result.values())

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
