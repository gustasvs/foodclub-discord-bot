import discord
from discord import app_commands
import random
import json
import sys
import datetime
import string
import asyncio

from utils.user_management_helpers import (
    load_profiles, 
    get_user_profile, 
    link_discord, 
    get_profile_from_discord, 
    update_remindme,
    update_snooze_remindme
    )
from utils.order_management_helpers import get_ratings, get_todays_orders, get_tracked_messages, save_tracked_message
from utils.helpers import emoji_to_value, value_to_emoji, community_report, random_answer, randomize_text    



def setup_commands(client: discord.Client):
    command_handler = app_commands.CommandTree(client)

    @command_handler.command(
        name="pause",
        description="Pause reminders for the day",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_remindme_snooze_command(interaction, paused: bool = True):
        await interaction.response.defer()
        profile = get_profile_from_discord(interaction.user.id, 'id-dc')
        if not profile:
            embed = discord.Embed(
                title=":link: Account Link Needed :link:",
                description="We couldn't find a Foodclub account linked to your Discord. Please use the `!link` command to connect your accounts.",
                color=0xFF5555
            )
            await interaction.followup.send(embed=embed)
            return

        called_again, reminders_disabled = update_snooze_remindme(profile.get('user-id'), paused)
        
        embed_props = {
            (True, True): (":zzz: Reminders Already Snoozed :mute:", 
                        "Your reminders are still on hold. No changes made. They will resume automatically after one day.", 
                        0xFFA500),
            (True, False): (":sun_with_face: Reminders Already Active :loud_sound:", 
                            "Your reminders are already up and running! No changes made.", 
                            0x32CD32),
            (False, True): (":zzz: Reminders Snoozed :mute:", 
                            "Your reminders are now on hold. They will resume automatically after one day. :sleeping:", 
                            0xFFFF00),
            (False, False): (":sun_with_face: Reminders Resumed :loud_sound:",
                            "Your reminders are back in action! :sunrise_over_mountains:", 
                            0x00FF00)
        }
        
        if not reminders_disabled:
            title, description, color = embed_props[(called_again, paused)]
            embed = discord.Embed(title=title, description=description, color=color)
        
        else:
            action = "pause" if paused else "resume"
            embed = discord.Embed(
                title=f":leftwards_pushing_hand: Can't {action}",
                description="It looks like there was an issue with changing the state of your reminders. Please try again later or contact support if the problem persists.",
                color=0xFFFF00
            )

        await interaction.followup.send(embed=embed)


    @command_handler.command(
        name="remindme",
        description="Toggle reminders on/off",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_remindme_command(interaction):
        await interaction.response.defer()
        profile = get_profile_from_discord(interaction.user.id, 'id-dc')
        if not profile:
            embed = discord.Embed(
                title=":mag_right: Link Required :link:",
                description="We couldn't find a Foodclub account linked to your Discord. Please use the `!link` command to connect your accounts.",
                color=0xFF0000
            )
            await interaction.followup.send(embed=embed)

        remindme = update_remindme(profile.get('user-id'))
        if remindme:
            embed = discord.Embed(
                title=":white_check_mark: Reminders Activated :bell:",
                description="You will now recieve a lot of reminders each morning until you order something!!!",
                color=0x00FF00
            )
        else:
            embed = discord.Embed(
                title=":octagonal_sign: Reminders Deactivated :no_bell:",
                description="You will no longer receive reminders. :(",
                color=0xFFFF00
            )
        await interaction.followup.send(embed=embed)


    @command_handler.command(
        name="extract",
        description="Extracts ratings from a channel and saves them to a file",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_extract_command(interaction):
        await interaction.response.defer()
        rating_history = {}
        count = 0
        async for history_message in interaction.followup.history(limit=200):
            for reaction in history_message.reactions:
                async for user in reaction.users():

                    rating = emoji_to_value(reaction.emoji)
                    if rating != 0:
                        if history_message.content not in rating_history:
                            rating_history[history_message.content] = []
                        count += 1
                        rating_history[history_message.content].append({'name-dc': user.name, 'id-dc': user.id, 'rating': rating, 'date': history_message.created_at.strftime("%Y-%m-%d")})
                    
        print(rating_history)
        # write in file
        with open("secret/rating_history.json", "w") as file:
            json.dump(rating_history, file, indent=4)
        await interaction.followup.send(f"extracted {count} ratings")

    @command_handler.command(
        name="link",
        description="links discord user with foodclub user",
        guild=discord.Object(id=1221861873532797078)
    )
    @app_commands.describe(discord_profile="User's Discord profile", foodclub_user_name="User's Foodclub profile name")
    async def handle_link_command(interaction, discord_profile: discord.User, foodclub_user_name: str):
        try:
            await interaction.response.defer()
            if not discord_profile:
                embed = discord.Embed(title="⚠️ Error ⚠️", color=0xe74c3c)
                embed.add_field(name="Part 1: discord user", value=f"use `@mention` feature\n\n**Example:** link `@Someone` Foodclub User", inline=True)
                embed.add_field(name="Part 2: foodclub user", value=f"after @mentioning a discord user, write foodclub users name\n\n**Example:** link @Someone `Foodclub User`", inline=False)
                # embed.add_field(name="Need Further Assistance?", value="If you're still encountering issues or have any questions, don't hesitate to reach out to our support team. We're here to help!", inline=False)
                await interaction.followup.send(embed=embed)
                return
            
            discord_id = discord_profile.id
            user_profile = get_user_profile(foodclub_user_name, 'name-fc')
            if user_profile is None:
                embed = discord.Embed(color=0xe74c3c)
                embed.add_field(name="User not found", value=f"User {foodclub_user_name} not found in the database", inline=False)
                embed.add_field(name="Dont know users?", value="Use `profiles` command to see all users", inline=False)
                await interaction.followup.send(embed=embed)
            else:
                foodclub_user_id = user_profile.get('user-id')
                link_discord(foodclub_user_id, discord_id, discord_profile.name)
                await interaction.followup.send(f":chains:  {foodclub_user_name} :chains: <@{discord_id}> :chains: ")
        except Exception as e:
            await interaction.followup.send("An error occurred while processing your request.")
            print(f"An error occurred: {e}")

    def assign_nuanced_ratings(dish_scores, max_score):
        # Define thresholds for nuanced ratings
        thresholds = {
            '💎': 0.95, '🇸': 0.9, '🇦➕': 0.85, '🇦': 0.8, '🇦➖': 0.75,
            '🇧➕': 0.7, '🇧': 0.65, '🇧➖': 0.6,
            '🇨➕': 0.55, '🇨': 0.5, '🇨➖': 0.45,
            '🇩➕': 0.4, '🇩': 0.35, '🇩➖': 0.3,
            '☢️🆘☕': 0.0
        }


        for dish, info in dish_scores.items():
            normalized_score = info['final_score'] / max_score if max_score else 0
            # Assign ratings based on normalized score
            for rating, threshold in thresholds.items():
                if normalized_score >= threshold:
                    info['rating'] = rating
                    break

    
    @command_handler.command(
        name="ratings",
        description="Displays the ratings for dishes",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_ratings_command(message):
        dish_scores, max_score = get_ratings()

        assign_nuanced_ratings(dish_scores, max_score)

        embed = discord.Embed(color=0x3498db)
        category_dishes = {}

        for dish, info in dish_scores.items():
            category = info['category']
            rating = info['rating']
            category_dishes.setdefault(category, []).append((dish, rating, info['final_score']))

        for category, dishes in sorted(category_dishes.items()):
            dishes_sorted = sorted(dishes, key=lambda x: x[2], reverse=True)
            dishes_display_str = "\n".join([f"- {dish} {rating}" for dish, rating, score in dishes_sorted]) #,  {score:.2f}||)
            embed.add_field(name=f"{category}", value=dishes_display_str[:1024], inline=False)

        await message.channel.send(embed=embed)

        # sorted_ratings = sorted(ratings.items(), key=lambda x: x[0], reverse=True)
        
        # embed = discord.Embed(color=0x3498db)
        
        # for rating_value, dish_infos in sorted_ratings:
        #     category_dishes = {}  # Organize dishes by category
        #     seen_dishes = {}

        #     for dish_info in dish_infos:
        #         if not seen_dishes.get(dish_info.get('title')):
        #             category_dishes.setdefault(dish_info.get('category'), []).append(dish_info.get('title'))
        #         seen_dishes[dish_info.get('title')] = True
            
        #     sorted_categories = sorted(category_dishes.items())

        #     dishes_display = []
        #     for category, dishes in sorted_categories:
        #         category_dishes_str = f"**{category}**\n" + "\n".join([f"- {dish}" for dish in dishes])
        #         dishes_display.append(category_dishes_str)
            
        #     dishes_display_str = "\n".join(dishes_display)
        #     dishes_display_str = dishes_display_str[:1024]  # Limit to 1024 characters
        #     embed.add_field(name=f"{value_to_emoji(rating_value)}", value=dishes_display_str, inline=False)

        # await message.channel.send(embed=embed)

    @command_handler.command(
        name="profiles",
        description="Displays the list of users",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_profiles_command(interaction):
        await interaction.response.defer()
        profiles = load_profiles()
        embed = discord.Embed(title=":yum: Bot user list: :pizza:", color=0x2ecc71)

        name_column = ""
        discord_username_column = ""

        for profile in profiles:
            name_column += f"{profile.get('name-fc', 'N/A')}\n"
            discord_username_column += f"{profile.get('name-dc', 'N/A')}\n"

        if len(name_column) > 1024 or len(discord_username_column) > 1024:
            # WIP: Split the data into multiple embeds if it exceeds the character limit
            pass
        else:
            embed.add_field(name="Foodclub name", value=name_column, inline=True)
            embed.add_field(name="Discord Username", value=discord_username_column, inline=True)

        await interaction.followup.send(embed=embed)

    @command_handler.command(
        name="orders",
        description="Displays the orders for the day",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_orders_command(interaction):

        await interaction.response.defer()

        todays_orders = get_todays_orders()

        if not todays_orders or len(todays_orders) == 0:
            await interaction.followup.send("No orders were made today.")
            return

        # get unique orders
        unique_orders = {order['dish-id']: order for order in todays_orders}.values()
        
        # categorise orders
        categorised_orders = {}
        for order in unique_orders:
            category = order['dish-category-title']
            if category in categorised_orders:
                categorised_orders[category].append(order)
            else:
                categorised_orders[category] = [order]

        # sort orders by dish title in each category
        for category, orders in categorised_orders.items():
            sorted_orders = sorted(orders, key=lambda x: x['dish-title'])
            categorised_orders[category] = sorted_orders

        await interaction.followup.send("Orders for the day:")
        for category, orders in categorised_orders.items():
            # for target in targets:
            await interaction.channel.send(f"**{category}**")
            for order in orders:
                order_message = f"- {order['dish-title']}"
                sent_message = await interaction.channel.send(order_message)
                save_tracked_message(sent_message.id, order)

    @command_handler.command(
        name="spam",
        description="Sends repeated messages to a user",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_spam_command(interaction, discord_user: discord.User, message_content: str):
        try:
            await interaction.response.defer()
            mention_id = discord_user.id
            await interaction.followup.send(f"Spamming <@{mention_id}>")
            for _ in range(5):
                await discord_user.send(
                    f"<@{mention_id}> message from {interaction.user.name} \n-->       ***{message_content}***        <--"
                )
        except Exception as e:
            await interaction.followup.send("The user is not valid.")
            # print(f"An error occurred: {e}")

    # async def handle_online_command(message, current_guild):
    #     online, afk, offline = community_report(current_guild)
    #     on = []
    #     for mem in current_guild.members:
    #         print(mem.status)
    #         if str(mem.status) != "offline":
    #             on.append(mem.name.lower())
    #     on.sort()
    #     messageee = str()
    #     for mem in on:
    #         messageee += str(mem) + "\n"
    #     messageee += f"```AFK: {afk}\nOffline: {offline}```"
    #     await message.channel.send(f"{messageee}")

    async def handle_total_command(message, current_guild):
        await message.channel.send(f"```{current_guild.member_count}```")


    @command_handler.command(
        name="help",
        description="Displays the list of commands",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_help_command(interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="Dzimtzemnieka kontroles 𓍯🧑🏾‍🌾", color=0x3498db)
        # embed.set_footer(text=":pizza: Foodclub bot :pizza:")
        embed.add_field(name="👥 user commands", value="`link`\n`users/profiles`", inline=False)
        embed.add_field(name="🍽️ foodclub commands", value="`ratings`\n`orders`\n`remindme`\n`pause/resume`\n`extract`", inline=False)
        embed.add_field(name="util commands", value="`spam`\n`online`\n`total`\n`logout`\n`exit`\n`help`", inline=False)
        await interaction.followup.send(embed=embed)

    async def handle_exit_command(message, client, admin_name, admin_required):
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
            embed = discord.Embed(
                title="Permission denied 🚫",
                description="It appears you do not have the necessary permissions to execute this command.",
                color=0xFF5733,
            )
            await message.channel.send(embed=embed)


    @command_handler.command(
        name="reminder",
        description="Set a reminder for a specified message after a certain duration",
        guild=discord.Object(id=1221861873532797078)
    )
    async def handle_reminder_command(interaction, reminder_message: str, time_in_minutes: int):
        await interaction.response.defer()
        reminder_time_in_seconds = time_in_minutes * 60
        if time_in_minutes < 1:
            await interaction.followup.send("Please enter a time greater than 1 minute.")
            return
        if time_in_minutes < 60:
            await interaction.followup.send(f"Reminder set for {time_in_minutes} minutes.")
        else:
            await interaction.followup.send(f"Reminder set for {time_in_minutes // 60} hours and {time_in_minutes % 60} minutes.")
        await asyncio.sleep(reminder_time_in_seconds)

        await interaction.user.send(f":exclamation: You set a reminder before {time_in_minutes} minutes. :exclamation: \n**{reminder_message}**")
        await interaction.followup.send(f"Reminder: {reminder_message}")
        

    return command_handler


async def handle_orders_command(targets):

    todays_orders = get_todays_orders()

    if not todays_orders or len(todays_orders) == 0:
        for target in targets:
            await target.send("No orders were made today.")
        return

    # get unique orders
    unique_orders = {order['dish-id']: order for order in todays_orders}.values()
    
    # categorise orders
    categorised_orders = {}
    for order in unique_orders:
        category = order['dish-category-title']
        if category in categorised_orders:
            categorised_orders[category].append(order)
        else:
            categorised_orders[category] = [order]

    # sort orders by dish title in each category
    for category, orders in categorised_orders.items():
        sorted_orders = sorted(orders, key=lambda x: x['dish-title'])
        categorised_orders[category] = sorted_orders

    for category, orders in categorised_orders.items():
        for target in targets:
            await target.send(f"**{category}**")
            for order in orders:
                order_message = f"- {order['dish-title']}"
                sent_message = await target.send(order_message)
                save_tracked_message(sent_message.id, order)