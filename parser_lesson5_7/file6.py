import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from tqdm import tqdm

URL = 'https://parsinger.ru/infiniti_scroll_2/'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _scroll(self, browser):
        target = browser.find_element(By.ID, "scroll-wrapper"). \
            find_element(By.ID, "scroll-container")
        flag = True
        result = list()
        while flag:
            try:
                el = target.find_element(By.TAG_NAME, "p")
                ic(el.text)
                result.append(int(el.text))
                while flag:
                    try:
                        patch = ".//following-sibling::*[1]"
                        el = el.find_element(By.XPATH, patch)
                        ic(el.text)
                        result.append(int(el.text))
                        browser.execute_script("return arguments[0].scrollIntoView(true);", el)

                    except Exception as ex:
                        ic(ex)
                        flag = False
            except Exception as exx:
                ic(exx)
        return result

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)

            result = self._scroll(browser=browser)

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return sum(result), len(result)


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
