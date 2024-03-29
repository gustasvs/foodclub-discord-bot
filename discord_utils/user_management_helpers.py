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

def get_user_profile(value, field='user-id'):
    profiles = load_profiles()
    for profile in profiles:
        # print(profile)
        print(str(profile.get(field)), str(value), str(profile.get(field)) == str(value))
        if str(profile.get(field)) == str(value):
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

def update_remindme(user_id):
    profiles = load_profiles()
    for i, profile in enumerate(profiles):
        if profile.get('user-id') == str(user_id):
            new_remindme = not profile.get('remindme', False)
            profiles[i]['remindme'] = new_remindme
            save_profiles(profiles)
            return not new_remindme

def get_profile_from_discord(value, field='id-dc'):
    profiles = load_profiles()
    for profile in profiles:
        if profile.get(field) == value:
            return profile
    return None
