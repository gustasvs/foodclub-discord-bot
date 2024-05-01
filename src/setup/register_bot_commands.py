import requests
import json

def setup_commands(bot_id, token, bot):
    url = f"https://discord.com/api/v10/applications/{bot_id}/commands"
    json = {
        "name": "hello",
        "description": "Returns a greeting",
        "type": 1 # 1 for chat input, 2 for user context menu, 3 for message context menu
    }
    headers = {
        "Authorization": f"Bot {token}"
    }
    response = requests.post(url, headers=headers, json=json)
    print(response.json())


