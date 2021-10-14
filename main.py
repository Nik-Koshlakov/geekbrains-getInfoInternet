import pprint
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient


def fill_hrefs(array):
    result = []
    for el in array:
        try:
            result.append(el.get_attribute('href'))
        except EC.StaleElementReferenceException as err:
            print("fail tag")

    return result


def load_next_letters(temp_array):
    actions = ActionChains(driver)
    actions.move_to_element(temp_array[-1])
    actions.perform()
    time.sleep(1)


chrome_options = Options()
#chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')

# вход в почту
input_login = driver.find_element(By.NAME, "login")
input_login.send_keys('study.ai_172@mail.ru')

button_input_pass = driver.find_element(By.XPATH, "//button[@data-testid='enter-password']")
button_input_pass.send_keys(Keys.ENTER)

time.sleep(3)

input_pass = driver.find_element(By.NAME, "password")
input_pass.send_keys('NextPassword172???')
button_input_to_mail = driver.find_element(By.XPATH, "//button[@data-testid='login-to-mail']")
button_input_to_mail.send_keys(Keys.ENTER)

# вытаскивание ссылок на письма
time.sleep(30)
"""
try:
    array = WebDriverWait(driver, 30)\
        .until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='dataset__items']/a")))
except:
    # driver.quit()
    print("Интернету плохо")
"""


href_letters = []
temp_array = []
array = []

while True:
    temp_array = driver.find_elements(By.XPATH, "//div[@class='dataset__items']/a")

    i = 1
    max_retry = 3
    while array and array[-1] == temp_array[-1] and i <= max_retry:
        load_next_letters(temp_array)
        temp_array = driver.find_elements(By.XPATH, "//div[@class='dataset__items']/a")
        i += 1

    if i >= max_retry:
        break

    if not array:
        load_next_letters(temp_array)
        href_letters += fill_hrefs(temp_array)
        array = temp_array.copy()
        temp_array.clear()
        continue

    if i == 1:
        load_next_letters(temp_array)

    href_letters += fill_hrefs(temp_array)
    array = temp_array.copy()
    temp_array.clear()

# прохождение по каждому письму и сохранение в бд
final_href_letters = list(dict.fromkeys(href_letters))
messages = []
for letter in final_href_letters:
    driver.get(letter)
    if final_href_letters.index(letter) == 20:
        break
    try:
        el = WebDriverWait(driver, 30) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "thread__subject")))
    except:
        continue
    finally:
        subject = el.text
        _from = driver.find_element(By.CLASS_NAME, "letter-contact").get_attribute('title')
        _date = driver.find_element(By.CLASS_NAME, "letter__date").text
        body = driver.find_element(By.CLASS_NAME, "letter__body").text
        messages.append({
            "from": _from,
            "date": _date,
            "subject": subject,
            "body_letter": body
        })

pprint(messages)
print("\n---------------------------------------------\n")

client = MongoClient('localhost', 27017)
db = client['parserWebSites']

if 'letters' in db.list_collection_names():
    db['letters'].drop()

letters_db = db['letters']
letters_db.insert_many(messages)

driver.close()