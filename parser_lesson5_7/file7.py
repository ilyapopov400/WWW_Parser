import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from tqdm import tqdm

URL = 'https://parsinger.ru/infiniti_scroll_3/'


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _scroll(self, browser, window):
        target = window.find_element(By.TAG_NAME, "div")
        flag = True
        result = list()
        while flag:
            try:
                el = target.find_element(By.TAG_NAME, "span")
                ic(el.text)
                result.append(int(el.text))
                while flag:
                    try:
                        actions = ActionChains(browser)  # скролим на 300 единиц
                        actions.move_to_element(el)
                        actions.scroll_by_amount(delta_x=0, delta_y=300).perform()

                        patch = ".//following-sibling::*[1]"
                        el = el.find_element(By.XPATH, patch)
                        result.append(int(el.text))

                    except Exception as ex:
                        ic(ex)
                        flag = False
            except Exception as exx:
                ic(exx)
        return result

    def _get_windows(self, browser) -> list:
        '''
        получаем список окон для дальнейшей прокрутки
        :param browser:
        :return:
        '''
        windows = browser.find_element(By.TAG_NAME, "body"). \
            find_element(By.CLASS_NAME, "main").find_elements(By.XPATH, "./div")
        return windows

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(URL)
            ic(browser.execute_script("return document.documentURI;"))

            windows = self._get_windows(browser=browser)
            result = 0
            for window in windows:
                result += sum(self._scroll(browser=browser, window=window))

            time.sleep(3)
            return result

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
