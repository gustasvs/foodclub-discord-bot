import json
from public.settings import USER_PROFILES_PATH

def load_profiles():
    try:
        with open(USER_PROFILES_PATH, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        print("No user profiles found")
        return []

def save_profiles(data):
    with open(USER_PROFILES_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def get_user_profile(value, field='email-fc'):
    profiles = load_profiles()
    for profile in profiles:
        if profile.get(field) == str(value):
            return profile
    return None

def set_user_profile(user_id, data):
    """Set user profile data"""
    profiles = load_profiles()
    exists = False
    for i, profile in enumerate(profiles):
        if profile.get('user-id') == user_id:
            exists = True 
    if not exists:
        profiles.append(data)
        print("ADDED NEW PROFILE: ", data)
        save_profiles(profiles)

def link_discord(user_id, discord_id, discord_name):
    profiles = load_profiles()
    for i, profile in enumerate(profiles):
        if profile.get('user-id') == str(user_id):
            profiles[i]['id-dc'] = discord_id
            profiles[i]['name-dc'] = discord_name
            save_profiles(profiles)
            return True
    return False

def get_profile_from_discord_id(discord_id):
    profiles = load_profiles()
    for profile in profiles:
        if profile.get('id-dc') == discord_id:
            return profile
    return None
