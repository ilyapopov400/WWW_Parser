import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic

with webdriver.Chrome() as driver:
    driver.get('https://parsinger.ru/selenium/1/1.html')
    form_first_name = driver.find_element(By.NAME, "first_name").send_keys("Ilya")
    form_last_name = driver.find_element(By.NAME, "last_name").send_keys("Popov")
    form_patronymic = driver.find_element(By.NAME, "patronymic").send_keys("Vladimirovich")
    form_age = driver.find_element(By.NAME, "age").send_keys("48")
    form_city = driver.find_element(By.NAME, "city").send_keys("Volgograd")
    form_email = driver.find_element(By.NAME, "email").send_keys("il_pop@mail.ru")

    form_button = driver.find_element(By.ID, "btn").click()

    form_result = driver.find_element(By.ID, "result").text

    time.sleep(2)
    ic(form_result)
