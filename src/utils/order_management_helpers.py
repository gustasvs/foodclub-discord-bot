import json
from datetime import datetime

from public.settings import ORDER_PATH, TRACKED_MESSAGES_PATH
from fetch_foodclub import get_data

def get_current_day():
    # 28.03.2024. should return 2148
    # 29.03.2024. should return 2149
    # 30.04.2024. should return 2227
    # etc 
    base_date = datetime(2024, 5, 1)
    current_date = datetime.now()
    delta = current_date - base_date
    return 2227 + delta.days

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

def rate_order_by_dish_title(dish_title, user_id, rating, date):
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = {}

    for dish_id, dish_info in orders.items():
        if dish_info['dish-title'] == dish_title:
            # Check if the exact rating already exists
            if any(r['user-id'] == user_id and r['date'] == date and r['rating'] == rating for r in dish_info.get('dish-ratings', [])):
                print(f"Duplicate rating for {dish_title} by {user_id} on {date}.")
                return
            else:
                print(f"Rated {dish_title} with {rating} by {user_id}")
                dish_info.setdefault('dish-ratings', []).append({
                    'user-id': user_id,
                    'rating': rating,
                    'date': date
                })
                with open(ORDER_PATH, 'w') as file:
                    json.dump(orders, file, indent=4)
                return

    print(f"Could not find dish {dish_title} to rate. ({user_id}, {rating}, {date})")


def rate_order(dish_id, user_id, rating, date):
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = {}

    if dish_id in orders:
        orders[dish_id]['dish-ratings'].append({
            'user-id': user_id,
            'rating': rating,
            'date': date
        })

    with open(ORDER_PATH, 'w') as file:
        json.dump(orders, file, indent=4)

def remove_rate_order(dish_id, user_id, rating, date):
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = {}

    if dish_id in orders:
        orders[dish_id]['dish-ratings'] = [
            r for r in orders[dish_id].get('dish-ratings', [])
            if not (r['user-id'] == user_id and r['rating'] == rating and r['date'] == date)
        ]

    with open(ORDER_PATH, 'w') as file:
        json.dump(orders, file, indent=4)

def get_ratings():
    try:
        with open(ORDER_PATH, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    scores = {}
    

    for dish_id, dish_info in orders.items():
        for rating_info in dish_info['dish-ratings']:
            score = rating_info['rating']
            title = dish_info['dish-title']

            if title in scores:
                scores[title]['score'] += score
                scores[title]['count'] += 1
            else:
                scores[title] = {'score': score, 'count': 1, 'category': dish_info['dish-category-title']}

    max_score = 0
    # average score multiplied by the times rated as to value better most popularily rated dishes
    for title, info in scores.items():
        info['final_score'] = (info['score'] / info['count']) + (info['count'] / 3)
        if info['final_score'] > max_score:
            max_score = info['final_score']
        

    return scores, max_score

    # output = {}
    # for dish_id, dish_info in orders.items():
    #     for rating_info in dish_info['dish-ratings']:
    #         rating = rating_info['rating']  # Extract the rating value
    #         # Initialize the list for this rating if it doesn't exist
    #         if rating not in output:
    #             output[rating] = []
    #         # Append the dish title to the list for this rating
    #         output[rating].append({'title': dish_info['dish-title'], 'category': dish_info['dish-category-title']})

    # return output

def get_tracked_messages():
    try:
        with open(TRACKED_MESSAGES_PATH, 'r') as file:
            tracked_messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
    return tracked_messages

def save_tracked_message(message_id, order):
    tracked_messages = get_tracked_messages()
    tracked_messages[message_id] = order
    with open(TRACKED_MESSAGES_PATH, 'w') as file:
        json.dump(tracked_messages, file, indent=4)

def get_todays_orders():
    day_id = get_current_day()
    print("Current day id: ", day_id)
    _, orders = get_data(day_id)
    return orders

def get_todays_users():
    day_id = get_current_day()
    print("Current day id: ", day_id)
    users, _ = get_data(day_id, refetch=True)
    # users, _ = get_data(2147)
    return users