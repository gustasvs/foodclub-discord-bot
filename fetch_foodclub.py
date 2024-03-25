
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
        url = f"https://api.lunch2.work/app/dishlists/history/525/{orders_id}?per_page=all&lang=lv"
        headers = {
            'Authorization': 'Bearer 95911|laravel_sanctum_cf5I2jrzVp2xRAha2MBCuJa3u956PMBbl3QkOmaA1b77b63b',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)

        data = response.json()

        print(data)

        users = []

        if 'orders' in data:
            for order in data['orders']:
                user_info = order.get('user', {})
                email = user_info.get('email', '')
                first_name = user_info.get('first_name', '')
                last_name = user_info.get('last_name', '')
                
                users.append({'email': email, 'first_name': first_name, 'last_name': last_name})


        for user in users:
            print(user)


    except Exception as e:
        wait(0, f"error: {e}")
        pass
    finally:
        pass


def set_local_storage(driver, data):
    for key, value in data.items():
        driver.execute_script(f"window.localStorage.setItem('{key}','{value}');")


if __name__ == "__main__":
    driver = webdriver.Firefox(service=Service(ff_webdriver_pth))

    driver.get(f'https://app.foodclub.lv/')

    wait(1, "loading page")    
    
    with open(f'secret/{cookies_name}.pkl', 'rb') as file:
        cookies = pickle.load(file) 
        for cookie in cookies:
            driver.add_cookie(cookie)

    with open(f'secret/{cookies_name}_local_storage.json', 'r') as file:
        local_storage_data = json.load(file)
        set_local_storage(driver, local_storage_data)

    wait(2, "Adding cookies and local storage")

    driver.get(f'https://app.foodclub.lv/')

    fetch_data(driver, 2132)
    driver.quit()
    pass 
    