import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')

with webdriver.Chrome(options=options_chrome) as driver:
    driver.get('https://parsinger.ru/selenium/3/3.html')
    forms = driver.find_elements(By.CLASS_NAME, "text")

    result = sum(map(lambda x: sum([int(i) for i in x.text.split()]), forms))
    ic(result)

    time.sleep(2)

with webdriver.Chrome(options=options_chrome) as driver:
    '''
    нет авторизации
    '''
    driver.get('https://stepik.org/lesson/709437/step/11?unit=710000')
    time.sleep(5)

