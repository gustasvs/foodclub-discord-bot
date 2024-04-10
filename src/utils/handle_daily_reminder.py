import discord
import random
from datetime import datetime

from utils.user_management_helpers import load_profiles
from utils.order_management_helpers import get_todays_users
from utils.bot_commands import handle_orders_command

channel_ids = [1221861873532797081]  

async def handle_daily_reminder(client, tracked_messages):
    now = datetime.now()
    print("Current time: ", now.hour, "-", now.minute, "-")
    if now.hour > 8 and (now.hour < 9 or (now.hour == 9 and now.minute < 30)):

        end_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
        remaining_time = end_time - now

        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes = remainder // 60

        if hours > 0:
            time_str = f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
        else:
            time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        
        profiles = load_profiles()
        already_ordered = get_todays_users()
        
        # filter out users who don't want to be reminded
        profiles = [profile for profile in profiles if profile.get('remindme', False) and not profile.get('snooze-remindme', False)]
        # print("Profiles to want to be reminded: ", profiles)
        # filter out users who already ordered
        for profile in profiles:
            for user in already_ordered:
                if profile.get('user-id') == user.get('user-id'):
                    print("Removing user who already ordered: ", profile.get('name-fc'))
                    profiles.remove(profile)
                    break
        # print("Profiles who have not ordered: ", profiles)

        # send reminder to all users
        random_food_emoji = random.choice(["🍜","🍕","🍔","🍟","🌭","🍦","🍩","🍪","🍫","🍬","🍭","🍮"])

        for profile in profiles:
            user_id = profile.get('user-id')
            discord_id = profile.get('id-dc')
            discord_user = client.get_user(discord_id)
            
            reminder_message = (
                    f"Good morning! 🌞 You have {time_str} "
                    f"left to place your food order for today. Don't miss out on a delicious meal! {random_food_emoji}"
                    f"\n\nIf you want to stop receiving reminders, type `pause`"
                )
            
            print(f"Sending reminder to {profile.get('name-fc')}")
            await discord_user.send(reminder_message)
    elif now.hour == 12 and now.minute < 10:
        channels = [client.get_channel(channel_id) for channel_id in channel_ids]
        await handle_orders_command(channels, tracked_messages)