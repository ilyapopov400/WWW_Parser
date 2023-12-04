import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')

with webdriver.Chrome(options=options_chrome) as driver:
    driver.get('https://parsinger.ru/selenium/3/3.html')
    forms = driver.find_elements(By.XPATH, "//div[@class='text']/p[2]")

    result = sum(map(lambda x: int(x.text), forms))
    ic(result)

    time.sleep(2)
