def emoji_number(number: int) -> str:
    emoji = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
    }
    return ''.join(emoji[char] for char in str(number))

def smart_number(number: float | int) -> float | int:
    return int(number) if isinstance(number, float) and number.is_integer() else number