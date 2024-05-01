#! before running this script you have to extract past ratings from a discord channel using "extract" command
import json
from utils.order_management_helpers import rate_order_by_dish_title
from utils.user_management_helpers import get_profile_from_discord
past_ratings = {}
with open("secret/rating_history.json", "r") as file:
    past_ratings = json.load(file)

for dish in past_ratings:
    # print(dish)
    for user in past_ratings[dish]:
        # print(user)
        foodclub_profile = get_profile_from_discord(user['name-dc'], 'name-dc')
        # print(foodclub_profile.get('user-id'))
        rate_order_by_dish_title(dish, foodclub_profile.get('user-id'), user['rating'], user['date'])
        