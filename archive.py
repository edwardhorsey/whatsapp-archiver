from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import os
import time

options = webdriver.ChromeOptions()
driver_path = f"user-data-dir=C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data/"
options.add_argument(driver_path)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://web.whatsapp.com/")

actions = ActionChains(driver)
ignored = StaleElementReferenceException

first_chat_location = "#pane-side > div:nth-child(1) > div > div > div:nth-child(1)"
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, first_chat_location)))
how_many_chats = driver.find_elements_by_class_name("_3ko75")

def format_nodes(arr):
    trim = [item for item in arr if item]
    return  [*trim[1:], trim[0]]

chat_names = format_nodes([chat.get_attribute('title') for chat in how_many_chats])
print(f'{len(chat_names)} unarchived chats: , {chat_names}')

def archive(user_name):
    try:
        user = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{user_name}"]')))
        actions.context_click(user).perform()
        # time.sleep(2) ?
        list = driver.find_element_by_xpath(f'//div[@title="Archive chat"]')
        list.click()
    except StaleElementReferenceException:
        print(f'User "{user_name}" is stale...')
    except Exception as e:
        driver.close()
        print(e)

for user in chat_names:
    if user:
        print(f'Archiving {user}')
        archive(user)
        # time.sleep(5) ?