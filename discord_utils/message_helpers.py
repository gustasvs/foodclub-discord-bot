import random
import string
import io
import sys
import discord

from guild_stats_helpers import community_report

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
        await message.channel.trigger_typing()
    except Exception as e:
        print(f"error: {e}")
        pass


    if "glogout" == msg.lower():
        if message.author.name == admin_name or admin_required == False:
            await message.channel.send(f"**logging out!**")
            await client.close()
            exit(0)
        else:
            await message.channel.send(f"*permission denied*")

    elif "gcrash" == msg.lower():
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

    elif "ghelp" in msg.lower():
        await message.channel.send(
            "```gspam - gspam @kuru\ncik on - cik on serveri\nkas on - kuri tiesi on\ncik vispar - cik vispar serveri dalibnieku\nglogout - izslegt botu\njebkura cita zina - bots pats izdoma ko atbildeet :D```"
        )

    elif "gspam" in msg.lower():
        mention_id = message.mentions[0].id
        target = client.get_user(mention_id)
        saturs = message.content[10 + len(str(mention_id)) :]
        await message.channel.send(f"Spamming <@{mention_id}>")
        for j in range(5):
            await target.send(
                f"<@{mention_id}> message from {message.author.name} \n-->       ***{saturs}***        <--"
            )

    elif "cik on" in msg.lower():
        online, afk, offline = community_report(current_guild)
        await message.channel.send(
            f"```Online - {online + afk}\nOffline - {offline}```"
        )

    elif "kas on" in msg.lower():
        on = []
        for mem in current_guild.members:
            if str(mem.status) != "offline":
                on.append(mem.name.lower())
        on.sort()
        messageee = str()
        for mem in on:
            messageee += str(mem) + "\n"
        await message.channel.send(f"```{messageee}```")

    elif "cik vispar" in msg.lower():
        await message.channel.send(f"```{current_guild.member_count}```")

    else:
        pass


def message_acceptable(message, bot_name=""):
    if message.author.name == bot_name:
        return False
    if str(message.content)[0] == "!":
        return False
    if message.author.bot:
        return False
    return True


def randomize_text(bot_answer):
    cip = random.randint(0, 7)
    if cip == 1:
        bot_answer += "*"
        bot_answer = "*" + bot_answer
    if cip == 2:
        bot_answer += "**"
        bot_answer = "**" + bot_answer
    if cip == 3:
        bot_answer += "***"
        bot_answer = "***" + bot_answer
    if cip == 4:
        random_emoji = random.choice(
            [
                ":smirk:",
                ":man_facepalming:",
                ":woman_facepalming:",
                ":chart_withdownwards_trend:",
                ":yum:",
                ":star_struck:",
                ":sob:",
                ":stuck_out_tongue_closed_eyes:",
                ":ok_hand:",
                ":partying_face:",
                ":rainbow:",
                ":boom:",
            ]
        )
        bot_answer += " " + random_emoji
    return bot_answer


def random_answer(message):
    return random.choice(
        [
            f"hello {message.author.name} !!!",
            ":smirk:",
        ]
    )
