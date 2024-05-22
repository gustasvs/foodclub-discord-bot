import io

from utils.user_management_helpers import get_profile_from_discord
from utils.order_management_helpers import save_order, rate_order, remove_rate_order, get_tracked_messages
from utils.helpers import emoji_to_value, value_to_emoji, community_report
from utils.transcription.transcriber import handle_audio_attachment

async def handle_reaction_add(client, reaction, user):

    tracked_messages = get_tracked_messages()

    await reaction.message.channel.typing()

    reaction_id = str(reaction.message.id)

    # print("Tracked messages: ", tracked_messages)

    # print("Reaction ID: ", reaction_id)


    if reaction_id in tracked_messages and user != client.user:
        print(reaction.emoji, str(reaction.emoji))
        reaction_value = emoji_to_value(str(reaction.emoji))

        user_profile = get_profile_from_discord(user.id, 'id-dc')
        if not user_profile:
            await reaction.message.channel.send(f"User {user.display_name} not found in database")
            return

        await reaction.message.channel.send(f"{user_profile.get('name-fc')} rated **{value_to_emoji(reaction_value)}** for dish {tracked_messages[reaction_id]['dish-title']}")

        date = reaction.message.created_at.strftime("%Y-%m-%d")

        rate_order(tracked_messages[reaction_id]['dish-id'], user_profile.get('user-id'), reaction_value, date)
    else:
        print("Reaction not found in tracked messages")
        # await reaction.message.channel.send("Reaction not found in tracked messages")


async def handle_reaction_remove(client, reaction, user):
    await reaction.message.channel.typing()

    tracked_messages = get_tracked_messages()

    reaction_id = str(reaction.message.id)

    if reaction_id in tracked_messages and user != client.user:
        print(f"Reaction {reaction.emoji} removed by {user.display_name}")
        reaction_value = emoji_to_value(str(reaction.emoji))

        user_profile = get_profile_from_discord(user.id, 'id-dc')  # Fetch user profile from your system
        if not user_profile:
            await reaction.message.channel.send(f"User {user.display_name} not found in database")
            return

        await reaction.message.channel.send(f"{user_profile.get('name-fc')} removed rating **{value_to_emoji(reaction_value)}** for dish {tracked_messages[reaction_id]['dish-title']}")

        date = reaction.message.created_at.strftime("%Y-%m-%d")

        remove_rate_order(tracked_messages[reaction_id]['dish-id'], user_profile.get('user-id'), reaction_value, date)


async def handle_on_message(
    client, message, bot_name, admin_name, admin_required, bot_id, current_guild
):
    if not message_acceptable(message, bot_name):
        return
    
    # if message had audio attachment handle it and return
    if await handle_audio_attachment(message): 
        return
    
    if message.content.startswith("transcribe"):
        print(message.reference)
        if message.reference is None:
            await message.channel.send("Please reply to a message to transcribe it.")
            return
        replied_message = message.reference.cached_message
        if replied_message is None:
            try:
                replied_message = await message.channel.fetch_message(message.reference.message_id)
            except: 
                await message.channel.send("Could not find the replied message.")
                return
        await handle_audio_attachment(replied_message)


    message_stats_for_logs = f"{message.channel}/{message.author} - {message.content}"
    with io.open("secret/log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message_stats_for_logs}\n")

    # generated_response = generate_response(message.content)

    # await message.channel.send(f"Message received: {message.content}")


def message_acceptable(message="", bot_name=""):
    if message.author.name == bot_name:
        return False
    if message.author.bot:
        return False
    return True
