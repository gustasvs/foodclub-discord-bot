import json

def load_profiles():
    try:
        with open('secret/user_profiles.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        print("No user profiles found")
        return []

def save_profiles(data):
    with open('secret/user_profiles.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_user_profile(user_id):
    profiles = load_profiles()
    return profiles.get(str(user_id), {})

def set_user_profile(user_id, data):
    """Set user profile data"""
    profiles = load_profiles()
    exists = False
    for i, profile in enumerate(profiles):
        if profile.get('email-fc') == str(user_id):
            exists = True 
    if not exists:
        profiles.append(data)
        print("ADDED NEW PROFILE: ", data)
        save_profiles(profiles)

def link_discord(user_id, discord_id, discord_name):
    profiles = load_profiles()
    for i, profile in enumerate(profiles):
        if profile.get('email-fc') == str(user_id):
            profiles[i]['id-dc'] = discord_id
            profiles[i]['name-dc'] = discord_name
            save_profiles(profiles)
            return True
    return False