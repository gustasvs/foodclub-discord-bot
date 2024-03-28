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