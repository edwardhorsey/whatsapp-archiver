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
user_profile = f"user-data-dir=C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data/"
options.add_argument(user_profile)

driver_path = ''
install = True
while install:
    try:
        driver_path = ChromeDriverManager().install()
        install = False
    except:
        install = True

driver = webdriver.Chrome(driver_path, options=options)
driver.get("https://web.whatsapp.com/")
handles = driver.window_handles

actions = ActionChains(driver)
ignored = StaleElementReferenceException

first_chat_location = "#pane-side > div:nth-child(1) > div > div > div:nth-child(1)"
first_chat_class = "_210SC"

def format_nodes(arr):
    trim = [item for item in arr if item]
    return  [*trim[1:], trim[0]]

def locate_chats():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, first_chat_location)))
    how_many_chats = driver.find_elements_by_class_name("_3ko75")
    chat_names = format_nodes([chat.get_attribute('title') for chat in how_many_chats])
    print(f'{len(chat_names)} unarchived chats: {chat_names}')
    return chat_names

def archive(user_name):
    try:
        user = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//span[@title="{user_name}"]')))
        actions.context_click(user).perform()
        time.sleep(1)
        list = driver.find_element_by_xpath(f'//div[@title="Archive chat"]')
        list.click()
    except StaleElementReferenceException:
        print(f'User "{user_name}" is stale...')
    except Exception as e:
        driver.close()
        print(e)

def archive_chats():
    chat_names = locate_chats()
    for user in chat_names:
        print(f'Archiving {user}')
        archive(user)
    chat_names = locate_chats()
    print(len(driver.window_handles))
    if chat_names:
        driver.execute_script("window.open('http://web.whatsapp.com/');")
        time.sleep(1)
        driver.close()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        archive_chats()

archive_chats()