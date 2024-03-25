import discord
import sys
import time
import datetime
from random import choice
import asyncio
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import io

from discord_utils.message_helpers import handle_on_message

# https://stackoverflow.com/questions/74071838/cant-receive-the-message-content-with-discord-bot
defIntents = discord.Intents.default()
defIntents.members = True
defIntents.message_content = True
client = discord.Client(intents=defIntents)

bot_credentials = open("secret/bot_credentials", "r").read()
bot_id = bot_credentials.split("\n")[0]
token = bot_credentials.split("\n")[1]


last_bot_answer = ""
current_guild_id = 1221861873532797078
current_guild = None

admin_required = True
admin_name = "gustasvs"
bot_name = "foodclub-bot"


@client.event
async def on_ready():
    global current_guild 
    current_guild = client.get_guild(current_guild_id)

    print(f"server name - {current_guild}")
    print(f"client info - {client.user}")

    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="latest foodclub.lv news"
        ),
    )



@client.event
async def on_message(message):
    try:
        print(f"Message content: {message.content}")
        await handle_on_message(
            client, message, bot_name, admin_name, admin_required, bot_id, current_guild
        )
    except Exception as e:
        print(f"error: {e}")
    finally:
        pass


client.run(token)
