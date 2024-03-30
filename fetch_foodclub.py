
import pickle
import requests
import time
import json
import os

from public.settings import CACHE_PATH

BUSINESS_FOODCLUB_ID = 525

# load foodclub token
foodclub_token = ''
with open(f'secret/foodclub_credentials', 'r') as file:
    foodclub_token = file.read()

def cache_response(response, filename):
    os.makedirs(CACHE_PATH, exist_ok=True)
    with open(f'{CACHE_PATH}/{filename}.pkl', 'wb') as file:
        pickle.dump(response, file)

def load_cached_response(filename):
    try:
        with open(f'{CACHE_PATH}/{filename}.pkl', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return None

def fetch_days_data(day_id):
    cached_data = load_cached_response(str(day_id))
    if cached_data is not None:
        print(f"Using cached data for day {day_id}")
        return cached_data

    try:
        url = f"https://api.lunch2.work/app/dishlists/history/{BUSINESS_FOODCLUB_ID}/{day_id}?per_page=all&lang=lv"
        headers = {
            'Authorization': foodclub_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            cache_response(data, str(day_id))
            return data
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_data(day_id):
    try:
        data = fetch_days_data(day_id)

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
        print(f"Error fetching data: {e}")
        return [], []


def set_local_storage(driver, data):
    for key, value in data.items():
        driver.execute_script(f"window.localStorage.setItem('{key}','{value}');")


if __name__ == "__main__":
    
    from discord_utils.user_management_helpers import set_user_profile
    from discord_utils.order_management_helpers import save_order

    for day_id in range(2080, 2148):
        print(f"Fetching data for day {day_id}")
        users, orders = get_data(day_id)

        for user in users:
            user_id = user['user-id']
            # print(f"Setting user profile for {user_id}")
            set_user_profile(user_id, user)

        for order in orders:
            save_order(order)
    