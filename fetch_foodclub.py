
import pickle
import requests
import time
import json
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from settings import *


def wait(sleep_len, message="", step=0, pbar=None):
    if pbar:
        pbar.update(step)
    if message:
        tqdm.write(message)
    time.sleep(sleep_len)

def fetch_data(driver, orders_id):
    try:
        driver.get(f'https://app.foodclub.lv/{orders_id}/')
        
        with open(f'secret/{cookies_name}.pkl', 'rb') as file:
            cookies = pickle.load(file) 
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.get('https://www.instagram.com/accounts/login')

        driver.find_element(by=By.XPATH, value="//button[text()='Not Now']").click()
        wait(1, "Skipping save login")
        driver.get(f'https://www.instagram.com/{orders_id}/')
        wait(7, "Getting followers")

    except Exception as e:
        wait(0, f"Error while following: {e}")
        pass
    finally:
        driver.quit()


def set_local_storage(driver, data):
    for key, value in data.items():
        driver.execute_script(f"window.localStorage.setItem('{key}','{value}');")


if __name__ == "__main__":
    driver = webdriver.Firefox(service=Service(ff_webdriver_pth))

    driver.get(f'https://app.foodclub.lv/')

    wait(3, "loading page")    
    
    with open(f'secret/{cookies_name}.pkl', 'rb') as file:
        cookies = pickle.load(file) 
        for cookie in cookies:
            driver.add_cookie(cookie)

    with open(f'secret/{cookies_name}_local_storage.json', 'r') as file:
        local_storage_data = json.load(file)
        set_local_storage(driver, local_storage_data)

    wait(2, "Adding cookies and local storage")

    driver.get(f'https://app.foodclub.lv/')

    wait(2, "LOGGED IN")
    # https://api.lunch2.work/app/dishlists/history/525/2132?per_page=all&lang=lv
    fetch_data(driver, 2132)
    driver.quit()
    pass 
    