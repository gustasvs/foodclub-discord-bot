
import pickle
import requests
import time
import json

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from public.settings import *
from discord_utils.user_profiles import set_user_profile

BUSINESS_FOODCLUB_ID = 525

# load foodclub token
foodclub_token = ''
with open(f'secret/foodclub_credentials', 'r') as file:
    foodclub_token = file.read()

def wait(sleep_len, message="", step=0, pbar=None):
    if pbar:
        pbar.update(step)
    time.sleep(sleep_len)

def fetch_data(orders_id):
    try:
        url = f"https://api.lunch2.work/app/dishlists/history/{BUSINESS_FOODCLUB_ID}/{orders_id}?per_page=all&lang=lv"
        headers = {
            'Authorization': foodclub_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = requests.get(url, headers=headers).json()

        users = []

        if 'orders' in data:
            for order in data['orders']:
                user_info = order.get('user', {})
                email = user_info.get('email', '')
                first_name = user_info.get('first_name', '')
                last_name = user_info.get('last_name', '')
                
                dishes = []
                for item in order.get('items', []):
                    dish_title = item.get('dish', {}).get('title', {}).get('lv', '')
                    dishes.append(dish_title)

                users.append({'email-fc': email, 'name-fc': first_name, 'last-name-fc': last_name}) # , 'dishes': dishes})
        return users


    except Exception as e:
        wait(0, f"error: {e}")
        pass
    finally:
        pass


def set_local_storage(driver, data):
    for key, value in data.items():
        driver.execute_script(f"window.localStorage.setItem('{key}','{value}');")


if __name__ == "__main__":
    # driver = webdriver.Firefox(service=Service(ff_webdriver_pth))

    # driver.get(f'https://app.foodclub.lv/')

    # wait(1, "loading page")    
    
    # with open(f'secret/{cookies_name}.pkl', 'rb') as file:
    #     cookies = pickle.load(file) 
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)

    # with open(f'secret/{cookies_name}_local_storage.json', 'r') as file:
    #     local_storage_data = json.load(file)
    #     set_local_storage(driver, local_storage_data)

    # wait(2, "Adding cookies and local storage")

    # driver.get(f'https://app.foodclub.lv/')

    users = fetch_data(2146)

    for user in users:
        user_id = user['email-fc']
        print(f"Setting user profile for {user_id}")
        set_user_profile(user_id, user)
    