import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands

from utils.helpers import get_bot_credentials, get_bot_intents, format_error_message
from utils.handle_message import handle_on_message, handle_reaction_add, handle_reaction_remove
from utils.handle_daily_reminder import handle_daily_reminder
# from setup.register_bot_commands import setup_commands
from utils.bot_commands import  setup_commands
from public.settings import *

client = discord.Client(command_prefix='$',intents=get_bot_intents())
command_handler = setup_commands(client)

bot_id, token = get_bot_credentials(BOT_CREDENTIALS_PATH)

@tasks.loop(minutes=10)
async def daily_reminder():
    await handle_daily_reminder(client)

@client.event
async def on_ready():
    global current_guild 
    current_guild = client.get_guild(current_guild_id)

    await command_handler.sync(guild=discord.Object(id=1221861873532797078))

    print(f"server name - {current_guild}")
    print(f"client info - {client.user}")

    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="foodclub orders 🍜"
        ),
    )

    daily_reminder.start() 

@client.event
async def on_message(message):
    try:
        print(f"Message content: {message.content}")
        await handle_on_message(
            client, 
            message, 
            bot_name, 
            admin_name, 
            admin_required, 
            bot_id, 
            current_guild
        )
    except Exception as e:
        print(f"error: {e}")
        await message.channel.send(format_error_message(e))

@client.event
async def on_reaction_add(reaction, user):
    try: 
        await handle_reaction_add(client, reaction, user)
    except Exception as e:
        print(f"error: {e}")
        await reaction.message.channel.send(format_error_message(e))

@client.event
async def on_reaction_remove(reaction, user):
    try:
        await handle_reaction_remove(client, reaction, user)
    except Exception as e:
        print(f"error: {e}")
        await reaction.message.channel.send(format_error_message(e))

try:
    client.run(token)
except:
    print("Failed to run client")
finally:
    pass