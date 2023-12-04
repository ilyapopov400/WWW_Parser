import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-data-dir=/Users/ilapopov/Library/Application Support/Google/Chrome/Default')
options_chrome.add_argument('--headless')

URL = 'https://parsinger.ru/selenium/4/4.html'

with webdriver.Chrome(options=options_chrome) as driver:
    driver.get(URL)
    form = driver.find_element(By.CSS_SELECTOR, "body")
    form = form.find_element(By.CLASS_NAME, "main")
    form = form.find_element(By.CLASS_NAME, "content")
    forms = form.find_elements(By.CLASS_NAME, "check")
    [f.click() for f in forms]

    button = driver.find_element(By.CSS_SELECTOR, "body")
    button = button.find_element(By.CLASS_NAME, "main")
    button = button.find_element(By.CLASS_NAME, "btn_box")
    button = button.find_element(By.CLASS_NAME, "btn")
    button.click()

    result = driver.find_element(By.ID, "result")
    ic(result.text)

    time.sleep(2)
