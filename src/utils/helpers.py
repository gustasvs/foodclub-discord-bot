import discord
import random

def community_report(guild):
    online = 0
    afk = 0
    offline = 0
    for mem in guild.members:
        if str(mem.status) == "online":
            online += 1
        if str(mem.status) == "offline":
            offline += 1
        else:
            afk += 1
    return online, afk, offline

def emoji_to_value(emoji):
    emoji_value_map = {
        "🇸": 7,
        "🇦": 6,
        "🇧": 5,
        "🇨": 4,
        "🇩": 3,
        "🇪": 2,
        "🇫": 1,
    }
    return emoji_value_map.get(emoji, 0)

def value_to_emoji(value):
    value_emoji_map = {
        7: "🇸",
        6: "🇦",
        5: "🇧",
        4: "🇨",
        3: "🇩",
        2: "🇪",
        1: "🇫",
    }
    return value_emoji_map.get(value, "N/A")

def get_bot_credentials(pth):
    bot_credentials = open(pth, "r").read()
    bot_id = bot_credentials.split("\n")[0]
    token = bot_credentials.split("\n")[1]
    return bot_id, token

def get_bot_intents():
    # https://stackoverflow.com/questions/74071838/cant-receive-the-message-content-with-discord-bot
    defIntents = discord.Intents.default()
    defIntents.members = True
    defIntents.message_content = True
    defIntents.guilds = True
    defIntents.guild_messages = True
    defIntents.guild_reactions = True
    defIntents.guild_typing = True
    defIntents.dm_messages = True
    defIntents.dm_reactions = True
    defIntents.dm_typing = True
    return defIntents

def format_error_message(error):
    return f""" 
*Something went ☕ ... * :( 
```bash
" - Error: {error}"
```
a || cheeky fix|| is required from the developer!"""


def randomize_text(bot_answer):
    def reverse_text(text):
        return text[::-1]

    def random_case(text):
        return ''.join(random.choice([char.upper(), char.lower()]) for char in text)

    def inject_emoji(text):
        emojis = [":smirk:", ":yum:", ":sob:", ":boom:", ":scream:", ":heart_eyes:", ":joy:", ":sunglasses:", ":fire:", ":ok_hand:"	]
        words = text.split()
        for _ in range(random.randint(1, 3)):
            words.insert(random.randint(0, len(words)), random.choice(emojis))
        return ' '.join(words)

    def decorate_text(text):
        decorations = ["`", "||"]
        decor = random.choice(decorations)
        return f"{decor}{text}{decor}"

    def add_punctuation(text):
        punctuations = ["!", "?", "..."]
        return text + random.choice(punctuations)

    def leet_speak(text):
        char_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
        return ''.join(char_map.get(c, c) if random.random() < 0.2 else c for c in text.lower())

    def scramble_words(text):
        def scramble(word):
            if len(word) > 3:
                middle = list(word[1:-1])
                random.shuffle(middle)
                return word[0] + ''.join(middle) + word[-1]
            return word
        return ' '.join(scramble(word) for word in text.split())

    def insert_random_words(text):
        fillers = ["like", "basically", "literally", "well", "um"]
        words = text.split()
        for _ in range(random.randint(1, 3)):
            words.insert(random.randint(0, len(words)), random.choice(fillers))
        return ' '.join(words)

    def quote_text(text):
        quotes = ["'{}'", '"{}"', '«{}»', '“{}”']
        return random.choice(quotes).format(text)

    def duplicate_characters(text):
        return ''.join(c + c if random.random() < 0.1 else c for c in text)

    def add_accentuation(text):
        accents = {'a': 'á', 'u': 'ú'}
        return ''.join(accents.get(c, c) for c in text.lower())

    transformations = [random_case, inject_emoji, decorate_text, add_punctuation, leet_speak,
        quote_text, duplicate_characters]

    # Randomly choose one or more transformations to apply
    chosen_transformations = random.sample(transformations, k=random.randint(1, len(transformations)))

    for transform in chosen_transformations:
        bot_answer = transform(bot_answer)

    return bot_answer


def random_answer(message):
    return random.choice(
        [
            f"hello {message.author.name} !!!",
            ":smirk:",
        ]
    )
