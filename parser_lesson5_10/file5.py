import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic
from tqdm import tqdm

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webcolors import rgb_to_name

URL = "https://parsinger.ru/selenium/5.10/3/index.html"


class Parser:
    dict_color = {'rgb(255, 0, 0)': 'red',
                  'rgb(0, 128, 0)': 'green',
                  'rgb(0, 0, 255)': 'blue',
                  'rgb(255, 255, 0)': 'yellow',
                  'rgb(128, 0, 128)': 'purple',
                  'rgb(255, 165, 0)': 'orange',
                  'rgb(255, 192, 203)': 'pink',
                  'rgb(165, 42, 42)': 'brown',
                  'rgb(128, 128, 128)': 'gray',
                  'rgb(0, 255, 255)': 'cyan'}

    def __init__(self, url: str):
        self.url = url
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument(
            'user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
        # self.options_chrome.add_argument('--headless')

    def _drag_and_drop(self, browser):
        browser.implicitly_wait(10)
        f = lambda x: x.get_attribute("style").split(";")[0].split(":")[-1].strip()
        actions = ActionChains(browser)

        squares_all = browser.find_element(By.CSS_SELECTOR, "div#main_container"). \
            find_elements(By.TAG_NAME, "div")  # все квадратики

        squares = browser.find_element(By.CSS_SELECTOR, "div#main_container"). \
            find_elements(By.CSS_SELECTOR, "div.draganddrop_end")  # пустые квадратики

        target_squares = filter(lambda x: ('draganddrop_end' not in x.get_attribute("class")),
                                squares_all)  # квадратики

        for target_square in target_squares:
            for square in squares:
                if f(target_square) == f(square):
                    actions.click_and_hold(target_square).move_to_element(square)
                    actions.release()
                elif "rgb" in f(target_square):
                    color = f(target_square).split("rgb")[-1]
                    color = color.strip("(")
                    color = color.strip(")")
                    color = tuple(int(item) for item in color.split(','))

                    color = rgb_to_name(color, spec='css3')

                    if color == f(square):
                        actions.click_and_hold(target_square).move_to_element(square)
                        actions.release()

        actions.perform()

    def _parser(self):
        with webdriver.Chrome(options=self.options_chrome) as browser:
            browser.implicitly_wait(10)
            browser.get(URL)

            self._drag_and_drop(browser=browser)

            time.sleep(3)

            return browser.find_element(By.CSS_SELECTOR, "p#message").text

    def run(self):
        result = self._parser()
        return result


if __name__ == "__main__":
    result = Parser(url=URL).run()
    ic(result)
