import discord

from discord_utils.handle_message import handle_on_message, handle_reaction_add, handle_reaction_remove
from public.settings import *

# https://stackoverflow.com/questions/74071838/cant-receive-the-message-content-with-discord-bot
defIntents = discord.Intents.default()
defIntents.members = True
defIntents.message_content = True
defIntents.guilds = True
defIntents.guild_messages = True
defIntents.guild_reactions = True
defIntents.guild_typing = True
defIntents.dm_messages = True
defIntents.dm_reactions = True
defIntents.dm_typing = True
client = discord.Client(intents=defIntents)

bot_credentials = open("secret/bot_credentials", "r").read()
bot_id = bot_credentials.split("\n")[0]
token = bot_credentials.split("\n")[1]

tracked_messages = {}

@client.event
async def on_ready():
    global current_guild 
    current_guild = client.get_guild(current_guild_id)

    print(f"server name - {current_guild}")
    print(f"client info - {client.user}")

    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="foodclub backend CPU's burn 🔥"
        ),
    )

@client.event
async def on_message(message):
    try:
        print(f"Message content: {message.content}")
        await handle_on_message(
            client, message, bot_name, admin_name, admin_required, bot_id, current_guild, tracked_messages
        )
    except Exception as e:
        print(f"error: {e}")
        error_message = f""" 
*Something went ☕ ... * :( 
```bash
" - Error: {e}"
```
a || cheeky fix|| is required from the developer!"""
        await message.channel.send(error_message)
    finally:
        pass

@client.event
async def on_reaction_add(reaction, user):
    await handle_reaction_add(client, reaction, user, tracked_messages)

@client.event
async def on_reaction_remove(reaction, user):
    await handle_reaction_remove(client, reaction, user, tracked_messages)

client.run(token)
