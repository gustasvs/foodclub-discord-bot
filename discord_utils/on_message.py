import random
import string
import io
import sys

from discord_utils.guild_stats_helpers import community_report
from discord_utils.user_management_helpers import load_profiles, set_user_profile, get_user_profile, link_discord
from bot_commands import (
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

async def handle_on_message(
    client, message, bot_name, admin_name, admin_required, bot_id, current_guild
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
            handle_link_command(message)

        case "ratings":
            handle_ratings_command(message)

        case "profiles" | "users":
            handle_profiles_command(message)

        case "orders":
            handle_orders_command(message)

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
            handle_help_command(message)

        case "spam":
            handle_spam_command(client, message)

        case "oneline":
            handle_online_command(message, current_guild)

        case "total":
            handle_total_command(message)
        
        case _:
            hanlde_default_command(message)


def message_acceptable(message, bot_name=""):
    if message.author.name == bot_name:
        return False
    if str(message.content)[0] == "!":
        return False
    if message.author.bot:
        return False
    return True
