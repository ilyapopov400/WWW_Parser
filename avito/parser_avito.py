import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.common.exceptions import NoAlertPresentException
from tqdm import tqdm
from itertools import product
from selenium.common.exceptions import NoSuchElementException

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
# options_chrome.add_argument('--headless')

URL = 'https://www.avito.ru'


class Parser:
    def __init__(self, url: str, to_find: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')
        self.to_find = to_find

    def _start_page(self, browser):
        '''
        работа со стартовой страницей,
        зашли в поиск, набрали что ищем, нажали кнопку "найти"
        :param driver:
        :return:
        '''
        form = browser.find_element(By.CLASS_NAME, "input-input-Zpzc1")
        form.send_keys(self.to_find)  # в поиск записали текст с to_find
        time.sleep(3)

        form = browser.find_element(By.CLASS_NAME, "desktop-9uhrzn")
        form.click()  # нажали кнопку "найти"
        time.sleep(3)

    def _one_page(self, browser):  # TODO
        # html_content = driver.page_source
        # soup = BeautifulSoup(html_content, 'html.parser')
        #
        # title = soup.find('title')

        try:
            result_text = str()
            text = browser.find_element(By.TAG_NAME, "body").find_element(By.ID, "app").find_element(By.CLASS_NAME,
                                                                                                     "style-item-description-html-qCwUL")

            text = text.find_elements(By.TAG_NAME, "p")
            for i in text:
                result_text += i.text

            ic(result_text)
        except NoSuchElementException as ex:
            ic(ex)
            time.sleep(1)

    def _list_pages(self, browser):
        '''
        со страницы, где расположен список найденных страниц, получаем отдельную страницу

        :param driver:
        :return:
        '''

        form = browser.find_element(By.CLASS_NAME, "styles-singlePageWrapper-eKDyt")
        form = form.find_element(By.CLASS_NAME, "styles-module-theme-CRreZ")
        form = form.find_element(By.CLASS_NAME, "index-root-KVurS")
        forms = form.find_elements(By.CLASS_NAME,
                                   "iva-item-title-py3i_")

        for it, page in enumerate(iterable=forms, start=1):  # проходим по страницам
            page.click()
            time.sleep(1)
            if it == 9:  # количество страниц, для отладки, потом убрать
                break

    def _go_to_windows(self, browser):
        '''
        проходим по открытым окнам
        '''
        for window in browser.window_handles:
            browser.switch_to.window(window)
            self._one_page(browser=browser)  # работа с открытым окном
            time.sleep(2)

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.get(self.url)

            self._start_page(browser=browser)  # открыли стартовую страницу сайта и ввели поиск
            time.sleep(1)

            self._list_pages(browser=browser)  # переходим по найденным ссылкам, открываем новые окна
            time.sleep(2)
            self._go_to_windows(browser=browser)  # проходим по открытым окнам

    def run(self):
        self._parser()
        return


def parser(url: str, to_find: str):
    with webdriver.Chrome(options=options_chrome) as driver:
        driver.get(url)

        form = driver.find_element(By.CLASS_NAME, "input-input-Zpzc1")
        form.send_keys(to_find)  # в поиск записали текст с to_find
        time.sleep(1)

        form = driver.find_element(By.CLASS_NAME, "desktop-9uhrzn")
        form.click()  # нажали кнопку "найти"
        time.sleep(1)

        step = 0  # количество пройденных страниц
        while True:
            try:
                step += 1
                down_form = driver.find_elements(By.CLASS_NAME,
                                                 "iva-item-title-py3i_")  # нашли ссылки на станицы
                for el in down_form:
                    el.click()
                    ic("Hello!")
                    time.sleep(1)

                form = driver.find_element(By.CLASS_NAME, "ArrowIcon-module-root_direction_right-zm8km")
                form.click()  # "ищем далее"
                time.sleep(1)
                break
            except Exception as ex:
                ic(ex)
                break

        ic(step)
        time.sleep(5)


if __name__ == "__main__":
    Parser(url=URL, to_find="Deep Purple lp").run()
    # parser(url=URL, to_find="Deep Purple LP")
