import discord

def emoji_to_value(emoji):
    emoji_value_map = {
        "🇸": 7,
        "🇦": 6,
        "🇧": 5,
        "🇨": 4,
        "🇩": 3,
        "🇪": 2,
        "🇫": 1,
    }
    return emoji_value_map.get(emoji, 0)

def value_to_emoji(value):
    value_emoji_map = {
        7: "🇸",
        6: "🇦",
        5: "🇧",
        4: "🇨",
        3: "🇩",
        2: "🇪",
        1: "🇫",
    }
    return value_emoji_map.get(value, "N/A")

def get_bot_credentials(pth):
    bot_credentials = open(pth, "r").read()
    bot_id = bot_credentials.split("\n")[0]
    token = bot_credentials.split("\n")[1]
    return bot_id, token

def get_bot_intents():
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
    return defIntents

def format_error_message(error):
    return f""" 
*Something went ☕ ... * :( 
```bash
" - Error: {error}"
```
a || cheeky fix|| is required from the developer!"""