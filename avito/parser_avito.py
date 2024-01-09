import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm
from itertools import product
from selenium.common.exceptions import NoSuchElementException


class ParserOnePage:
    '''
    парсинг одной страницы avito
    :return текст детального описания товара
    '''

    def __init__(self, browser):
        self.browser = browser

    def _target_text(self, browser) -> list:
        target_text = list()
        window = browser.find_element(By.CSS_SELECTOR, "div.style-item-description-pL_gy")
        for line in window.find_elements(By.TAG_NAME, "p"):
            target_text.append(line.text)
        return target_text

    def _parser(self) -> str:
        result = self._target_text(browser=self.browser)
        return ", ".join(result)

    def run(self) -> str:
        result = self._parser()
        return result


class Parser:
    url = 'https://www.avito.ru'

    def __init__(self, to_find: str, refinement_find: str = None):
        '''

        :param to_find: поисковый запрос
        :param refinement_find: уточнение поискового запроса, для поиска в описании товара
        '''
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')
        self.to_find = to_find
        self.refinement_find = refinement_find

    def _start_page(self, browser):
        '''
        работа со стартовой страницей,
        зашли в поиск, набрали "self.to_find" в поисковом запросе, нажали кнопку "найти"
        :param browser:
        :return:
        '''
        form = browser.find_element(By.CLASS_NAME, "input-input-Zpzc1")
        form.send_keys(self.to_find)  # в поиск записали текст с to_find
        time.sleep(3)

        form = browser.find_element(By.CLASS_NAME, "desktop-9uhrzn")
        form.click()  # нажали кнопку "найти"
        time.sleep(3)

    def _one_page(self, browser):
        '''
        работа с одной открытой страницы товара в браузере
        :param browser:
        :return:
        '''
        browser.implicitly_wait(5)
        try:
            text = ParserOnePage(browser=browser).run()
            return text
        except selenium.common.exceptions.NoSuchElementException as ex:
            ic(ex, browser.current_url)

    def _list_pages(self, browser):
        '''
        на странице, где расположен список найденных страниц, кликаем по всем ним

        :param browser:
        :return:
        '''
        browser.implicitly_wait(5)

        form = browser.find_element(By.CLASS_NAME, "styles-singlePageWrapper-eKDyt")
        form = form.find_element(By.CLASS_NAME, "styles-module-theme-CRreZ")
        form = form.find_element(By.CLASS_NAME, "index-root-KVurS")
        forms = form.find_elements(By.CLASS_NAME,
                                   "iva-item-title-py3i_")
        ic(len(forms))
        for it, page in enumerate(iterable=forms, start=1):  # проходим по страницам
            page.click()
            browser.implicitly_wait(5)
            time.sleep(10)

            if it == 3:  # TODO количество страниц, для отладки, потом убрать
                break

    def _go_to_windows(self, browser):
        '''
        проходим по открытым окнам
        '''
        browser.implicitly_wait(5)
        for window in browser.window_handles:
            browser.switch_to.window(window)
            text = self._one_page(browser=browser)  # работа с открытым окном
            ic(text)  # получили текст детального описания товара

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(self.url)
            browser.implicitly_wait(5)

            self._start_page(browser=browser)  # открыли стартовую страницу сайта и ввели поиск

            self._list_pages(browser=browser)  # переходим по найденным ссылкам, открываем новые окна

            self._go_to_windows(browser=browser)  # проходим по открытым окнам

    def run(self):
        self._parser()
        return


if __name__ == "__main__":
    Parser(to_find="Deep Purple lp").run()
