import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
options_chrome.add_argument('--headless')

URL = 'https://parsinger.ru/selenium/6/6.html'

with webdriver.Chrome(options=options_chrome) as driver:
    driver.get(URL)

    form = driver.find_element(By.ID, "text_box")
    result = eval(form.text)
    ic(result, type(result))

    form = driver.find_element(By.ID, "selectId")
    forms = form.find_elements(By.TAG_NAME, "option")
    form = list(filter(lambda x: int(x.text) == result, forms))
    form[0].click()

    form = driver.find_element(By.ID, "sendbutton")
    form.click()

    form = driver.find_element(By.ID, "result")
    ic(form.text)

    time.sleep(5)
