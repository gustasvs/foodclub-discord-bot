
import pickle
import requests
import time
import json

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from public.settings import *
from discord_utils.user_management_helpers import set_user_profile
from discord_utils.order_management_helpers import save_order, save_todays_orders

BUSINESS_FOODCLUB_ID = 525

# load foodclub token
foodclub_token = ''
with open(f'secret/foodclub_credentials', 'r') as file:
    foodclub_token = file.read()

def wait(sleep_len, message="", step=0, pbar=None):
    if pbar:
        pbar.update(step)
    time.sleep(sleep_len)

def fetch_days_data(day_id):
    try:
        url = f"https://api.lunch2.work/app/dishlists/history/{BUSINESS_FOODCLUB_ID}/{day_id}?per_page=all&lang=lv"
        headers = {
            'Authorization': foodclub_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = requests.get(url, headers=headers).json()

        users = []
        orders = []

        if 'orders' in data:
            for order in data['orders']:
                user_info = order.get('user', {})
                user_id = user_info.get('id', 0)
                user_email = user_info.get('email', '')
                first_name = user_info.get('first_name', '')
                last_name = user_info.get('last_name', '')
                
                users.append({'user-id': user_id, 'email-fc': user_email, 'name-fc': first_name, 'last-name-fc': last_name})

                for item in order.get('items', []):
                    dish_id = item.get('dish', {}).get('id', 0)
                    dish_title = item.get('dish', {}).get('title', {}).get('lv', '')
                    dish_category_title = item.get('dish', {}).get('category', {}).get('title', {}).get('lv', '')
                    dish_price = item.get('dish', {}).get('price', 0)
                    
                    user_order = {'day-id': day_id, 'user-id': user_id, 'dish-id': dish_id, 'dish-title': dish_title, 'dish-category-title': dish_category_title, 'dish-price': dish_price}
                    orders.append(user_order)

        return users, orders


    except Exception as e:
        wait(0, f"error: {e}")
        pass
    finally:
        pass


def set_local_storage(driver, data):
    for key, value in data.items():
        driver.execute_script(f"window.localStorage.setItem('{key}','{value}');")


if __name__ == "__main__":

    for day_id in range(2145, 2146):
        users, orders = fetch_days_data(day_id)

        save_todays_orders(orders)

        for user in users:
            user_id = user['user-id']
            print(f"Setting user profile for {user_id}")
            set_user_profile(user_id, user)

        for order in orders:
            save_order(order)
            # print(f"Order: {order}")
    