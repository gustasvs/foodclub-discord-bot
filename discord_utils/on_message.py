import random
import string
import io
import sys

from discord_utils.guild_stats_helpers import community_report
from discord_utils.user_management_helpers import get_profile_from_discord_id
from discord_utils.order_management_helpers import save_order, rate_order, get_ratings
from discord_utils.bot_commands import (
    handle_link_command,
    handle_ratings_command,
    handle_profiles_command,
    handle_orders_command,
    handle_help_command,
    handle_spam_command,
    handle_online_command,
    handle_total_command,
    hanlde_default_command,
)

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
        7: ":regional_indicator_s:",
        6: ":regional_indicator_a:",
        5: ":regional_indicator_b:",
        4: ":regional_indicator_c:",
        3: ":regional_indicator_d:",
        2: ":regional_indicator_e:",
        1: ":regional_indicator_f:",
    }
    return value_emoji_map.get(value, "N/A")

async def handle_reaction_add(client, reaction, user, tracked_messages):

    if reaction.message.id in tracked_messages and user != client.user:
        print(reaction.emoji, str(reaction.emoji))
        reaction_value = emoji_to_value(str(reaction.emoji))

        user_profile = get_profile_from_discord_id(user.id)
        if not user_profile:
            await reaction.message.channel.send(f"User {user.display_name} not found in database")
            return

        await reaction.message.channel.send(f"{user_profile.get('name-fc')} rated **{value_to_emoji(reaction_value)}** for dish {tracked_messages[reaction.message.id]['dish-title']}")

        rate_order(tracked_messages[reaction.message.id]['dish-id'], user_profile.get('user-id'), reaction_value)
        
        # tracked_messages[reaction.message.id]['votes'][user.display_name] = reaction_value
        # tracked_messages[reaction.message.id]['voters'].append(user.id)

        #* optional: remove the reaction after processing
        # await reaction.remove(user)

async def handle_on_message(
    client, message, bot_name, admin_name, admin_required, bot_id, current_guild, tracked_messages
):
    msg = message.content
    tagged = False
    if f"<@!{bot_id}>" in msg:
        msg = msg[len(bot_id) :]
        tagged = True

    message_stats_for_logs = f"{message.channel}/{message.author} - {msg}"
    with io.open("secret/log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message_stats_for_logs}\n")

    if not message_acceptable(message, bot_name):
        return
    
    try: 
        await message.channel.typing()
    except Exception as e:
        print(f"error: {e}")
        pass

    match msg.lower().split(" ")[0]:
        case "link":
            await handle_link_command(message)

        case "ratings":
            await handle_ratings_command(message)

        case "profiles" | "users":
            await handle_profiles_command(message)

        case "orders":
            await handle_orders_command(message, tracked_messages)

        case "logout":
            if message.author.name == admin_name or admin_required == False:
                await message.channel.send(f"**logging out!**")
                await client.close()
                exit(0)
            else:
                await message.channel.send(f"*permission denied*")

        case "exit":
            if message.author.name == admin_name or admin_required == False:
                letters = string.ascii_lowercase + string.ascii_uppercase
                mes = ""
                for e in range(random.randint(4, 12)):
                    streng = "".join(
                        random.choice(letters) for i in range(random.randint(2, 20))
                    )
                    if random.randint(1, 2) == 1:
                        cip = random.randint(1, 3)
                        if cip == 1:
                            streng = "*" + streng
                            streng += "*"
                        if cip == 2:
                            streng = "**" + streng
                            streng += "**"
                        if cip == 3:
                            streng = "***" + streng
                            streng += "***"

                    mes += streng
                    mes += "\n"
                await message.channel.send(mes)
                await message.channel.send(
                    "*error 0x0000003b*\nquitting aplication\n***quitti***\n*ng ap*"
                )
                await client.close()
                sys.exit()
            else:
                await message.channel.send(f"**permission denied**")

        case "help":
            await handle_help_command(message)

        case "spam":
            await handle_spam_command(client, message)

        case "online":
            await handle_online_command(message, current_guild)

        case "total":
            await handle_total_command(message, current_guild)
        
        case _:
            await hanlde_default_command(message)


def message_acceptable(message, bot_name=""):
    if message.author.name == bot_name:
        return False
    if str(message.content)[0] == "!":
        return False
    if message.author.bot:
        return False
    return True
