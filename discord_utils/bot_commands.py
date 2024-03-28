import discord
import random

from discord_utils.user_management_helpers import load_profiles, get_user_profile, link_discord
from discord_utils.guild_stats_helpers import community_report
from discord_utils.order_management_helpers import get_ratings
from discord_utils.order_management_helpers import get_todays_orders
from discord_utils.on_message import value_to_emoji

async def handle_link_command(message):
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
        foodclub_user_id = user_profile.get('user-id')
        link_discord(foodclub_user_id, discord_id, message.mentions[0].name)
        await message.channel.send(f":chains:  {foodclub_user_name} :chains: <@{discord_id}> :chains: ")


async def handle_ratings_command(message):
    ratings = get_ratings()

    embed = discord.Embed(title=":fork_knife_plate: Ratings :fork_knife_plate:", color=0x3498db)
    
    for rating, dishes in ratings.items():
        ratings[rating] = list(set(dishes))

    sorted_ratings = sorted(ratings.items(), key=lambda x: x[0], reverse=True)
    
    for rating_value, dishes in sorted_ratings:
        # Combine all dish titles for the current rating into a single string
        dishes_list = "\n".join(dishes)
        # Add a field to the embed with the rating value as the name and the dish titles as the value
        embed.add_field(name=f"{value_to_emoji(rating_value)}", value=dishes_list, inline=False)

    await message.channel.send(embed=embed)


async def handle_profiles_command(message):
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

async def handle_orders_command(message, tracked_messages):
    todays_orders = get_todays_orders()

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
        await message.channel.typing()
        await message.channel.send(f"**{category}**")
        for order in orders:
            order_message = f"- {order['dish-title']}"
            sent_message = await message.channel.send(order_message)
            tracked_messages[sent_message.id] = order

async def handle_spam_command(client, message):
    mention_id = message.mentions[0].id
    target = client.get_user(mention_id)
    saturs = message.content[10 + len(str(mention_id)) :]
    await message.channel.send(f"Spamming <@{mention_id}>")
    for _ in range(5):
        await target.send(
            f"<@{mention_id}> message from {message.author.name} \n-->       ***{saturs}***        <--"
        )

async def handle_online_command(message, current_guild):
    online, afk, offline = community_report(current_guild)
    on = []
    for mem in current_guild.members:
        print(mem.status)
        if str(mem.status) != "offline":
            on.append(mem.name.lower())
    on.sort()
    messageee = str()
    for mem in on:
        messageee += str(mem) + "\n"
    messageee += f"```AFK: {afk}\nOffline: {offline}```"
    await message.channel.send(f"{messageee}")

async def handle_total_command(message, current_guild):
    await message.channel.send(f"```{current_guild.member_count}```")

async def handle_help_command(message):
    embed = discord.Embed(title="🤖 Helpful Commands Guide 🤖", color=0x3498db)
    embed.set_thumbnail(url="https://example.com/bot_icon.png")  # Replace with your bot's icon URL
    embed.set_footer(text="Use these commands to interact with the bot. For more info, type command_name --help")

    # User-related commands
    embed.add_field(name="👥 User Commands",
                    value="`link @discord_user Foodclub User` - Links your Discord account to your Foodclub user.\n"
                          "`profiles` - Displays all Foodclub user profiles.\n",
                    inline=False)

    # Foodclub-related commands
    embed.add_field(name="🍽️ Foodclub Commands",
                    value="`ratings` - Shows dish ratings.\n"
                          "`orders` - Lists current food orders.\n",
                    inline=False)

    # Utility commands
    embed.add_field(name="🛠️ Utility Commands",
                    value="`spam @discord_user message` - Sends a spam message to a user.\n"
                          "`online` - Shows online members.\n"
                          "`total` - Displays the total number of guild members.\n",
                    inline=False)

    # Example usage
    embed.add_field(name="🔍 Example Usage",
                    value="`link @JohnDoe JohnDoeFC` - This will link the Discord user @JohnDoe to the Foodclub user 'JohnDoeFC'.",
                    inline=False)

    # Note about assistance
    embed.add_field(name="ℹ️ Need Further Assistance?",
                    value="If you have questions or need help with a specific command, you can reply to this message or contact an admin.",
                    inline=False)

    await message.channel.send(embed=embed)

async def hanlde_default_command(message):
    bot_answer = random_answer(message)
    bot_answer = randomize_text(bot_answer)
    await message.channel.send(bot_answer)

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
