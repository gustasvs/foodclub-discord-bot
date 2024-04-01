from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import pickle
import time
import json
from public.settings import *

driver = webdriver.Firefox(service=Service(FF_WEBDRIVER_PATH))

driver.get("https://app.foodclub.lv/")

time.sleep(20)

with open(f'secret/{cookies_name}.pkl', 'wb') as file:
    pickle.dump(driver.get_cookies(), file)

# Retrieve and save all key-value pairs from local storage
local_storage = driver.execute_script(
    "let ls = {}; "
    "for (let i = 0, len = localStorage.length; i < len; i++) { "
    "  let key = localStorage.key(i); "
    "  let value = localStorage.getItem(key); "
    "  ls[key] = value; "
    "} "
    "return ls; "
)

with open(f'secret/{cookies_name}_local_storage.json', 'w') as file:
    json.dump(local_storage, file)

driver.quit();