import json
from utils.order_management_helpers import rate_order_by_dish_title
from utils.user_management_helpers import get_profile_from_discord
past_ratings = {}
with open("secret/rating_history.json", "r") as file:
    past_ratings = json.load(file)

# {
#     "C\u016bkga\u013cas gula\u0161s s\u0113\u0146u \u2013 kr\u0113juma m\u0113rc\u0113": [
#         {
#             "name-dc": "tomslielkalns",
#             "id-dc": 996449602406449285,
#             "rating": 5,
#             "date": "2024-03-27"
#         }
#     ],
#     "D\u0101rze\u0146u sacepums": [
#         {
#             "name-dc": "tomslielkalns",
#             "id-dc": 996449602406449285,
#             "rating": 4,
#             "date": "2024-03-27"
#         }
#     ],
#     "Upe\u0146u kr\u0113ms ar vani\u013cas m\u0113rci": [
#         {
#             "name-dc": "gustasvs",
#             "id-dc": 419456995058253845,
#             "rating": 5,
#             "date": "2024-03-27"
#         }
#     ],

for dish in past_ratings:
    # print(dish)
    for user in past_ratings[dish]:
        # print(user)
        foodclub_profile = get_profile_from_discord(user['name-dc'], 'name-dc')
        # print(foodclub_profile.get('user-id'))
        rate_order_by_dish_title(dish, foodclub_profile.get('user-id'), user['rating'], user['date'])
        