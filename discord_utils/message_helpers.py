import random
import string
import io
import sys
import discord

from discord_utils.guild_stats_helpers import community_report
from discord_utils.user_profiles import load_profiles, set_user_profile, get_user_profile, link_discord

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
            profiles = load_profiles()
            if len(message.mentions) == 0:
                embed = discord.Embed(title="⚠️ Error ⚠️", color=0xe74c3c)
                embed.add_field(name="Part 1: discord user", value=f"use `@mention` feature\n\n**Example:** link `@Someone` Foodclub User", inline=True)
                embed.add_field(name="Part 2: foodclub user", value=f"after @mentioning a discord user, write foodclub users name\n\n**Example:** link @Someone `Foodclub User`", inline=False)
                # embed.add_field(name="Need Further Assistance?", value="If you're still encountering issues or have any questions, don't hesitate to reach out to our support team. We're here to help!", inline=False)
                await message.channel.send(embed=embed)
                return
            
            discord_id = message.mentions[0].id
            foodclub_user_name = message.content.split(" ", 2)[-1]
            user_profile = get_user_profile(foodclub_user_name, 'name-fc')
            if user_profile is None:
                embed = discord.Embed(color=0xe74c3c)
                embed.add_field(name="User not found", value=f"User {foodclub_user_name} not found in the database", inline=False)
                embed.add_field(name="Dont know users?", value="Use `profiles` command to see all users", inline=False)
                await message.channel.send(embed=embed)
            else:
                foodclub_user_email = user_profile.get('email-fc')
                link_discord(foodclub_user_email, discord_id, message.mentions[0].name)
                await message.channel.send(f":chains:  {foodclub_user_name} :chains: <@{discord_id}> :chains: ")

        case "profiles" | "users":
            profiles = load_profiles()
            embed = discord.Embed(title=":yum: Bot user list: :pizza:", color=0x2ecc71)

            name_column = ""
            discord_username_column = ""

            for profile in profiles:
                name_column += f"{profile.get('name-fc', 'N/A')}\n"
                discord_username_column += f"{profile.get('name-dc', 'N/A')}\n"

            if len(name_column) > 1024 or len(discord_username_column) > 1024:
                # Handle the case where content is too long (e.g., split into multiple embeds, truncate, etc.)
                pass
            else:
                embed.add_field(name="Foodclub name", value=name_column, inline=True)
                embed.add_field(name="Discord Username", value=discord_username_column, inline=True)

            await message.channel.send(embed=embed)

        
        case "orders":
            profiles = load_profiles()
            res = "Foodclub users:\n"
            for profile in profiles:
                res += str(profile.get('name')) + profile.get('discord_id') + "\n"
            await message.channel.send(f"```{res}```")

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
            await message.channel.send(
                f"```!logout - logs out\n!exit - exits\n!spam - spams user\n!howmany - shows online users\n!who - shows online users\n!total - shows total users```"
            )

        case "spam":
            mention_id = message.mentions[0].id
            target = client.get_user(mention_id)
            saturs = message.content[10 + len(str(mention_id)) :]
            await message.channel.send(f"Spamming <@{mention_id}>")
            for _ in range(5):
                await target.send(
                    f"<@{mention_id}> message from {message.author.name} \n-->       ***{saturs}***        <--"
                )

        case "howmany":
            online, afk, offline = community_report(current_guild)
            await message.channel.send(
                f"```Online - {online + afk}\nOffline - {offline}```"
            )

        case "who":
            on = []
            for mem in current_guild.members:
                if str(mem.status) != "offline":
                    on.append(mem.name.lower())
            on.sort()
            messageee = str()
            for mem in on:
                messageee += str(mem) + "\n"
            await message.channel.send(f"```{messageee}```")

        case "total":
            await message.channel.send(f"```{current_guild.member_count}```")
        
        case _:
            bot_answer = random_answer(message)
            bot_answer = randomize_text(bot_answer)
            await message.channel.send(bot_answer)


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
