import json
from public.settings import ORDER_PATH

def save_order(new_order):
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = {}

    dish_id = new_order['dish-id']
    
    if dish_id in orders:
        if not any(user['user-id'] == new_order['user-id'] and user['day-id'] == new_order['day-id'] for user in orders[dish_id]['consumers']):
            orders[dish_id]['consumers'].append({
                'user-id': new_order['user-id'],
                'day-id': new_order['day-id']
            })
    else:
        orders[dish_id] = {
            'dish-title': new_order['dish-title'],
            'dish-category-title': new_order['dish-category-title'],
            'dish-price': new_order['dish-price'],
            'dish-ratings': [],
            'consumers': [{
                'user-id': new_order['user-id'],
                'day-id': new_order['day-id']
            }]
        }
    with open(ORDER_PATH, 'w') as file:
        json.dump(orders, file, indent=4)

def rate_order(dish_id, user_id, rating):
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = {}

    if dish_id in orders:
        orders[dish_id]['dish-ratings'].append({
            'user-id': user_id,
            'rating': rating
        })

    with open(ORDER_PATH, 'w') as file:
        json.dump(orders, file, indent=4)

def get_ratings():
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    output = {}
    for dish_id, dish_info in orders.items():
        for rating_info in dish_info['dish-ratings']:
            rating = rating_info['rating']  # Extract the rating value
            # Initialize the list for this rating if it doesn't exist
            if rating not in output:
                output[rating] = []
            # Append the dish title to the list for this rating
            output[rating].append(dish_info['dish-title'])

    return output

def save_todays_orders(orders):
    # rewrites existing todays orders
    with open('secret/todays_orders.json', 'w') as file:
        json.dump(orders, file, indent=4)

def get_todays_orders():
    try:
        with open('secret/todays_orders.json', 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return orders