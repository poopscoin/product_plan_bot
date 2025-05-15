from telegram import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers, InlineKeyboardButton, InlineKeyboardMarkup
from mlangm import translate as _

class BaseKeyboard:
    buttons_per_page = 8
    nav_variants = [[KeyboardButton("<-")], [KeyboardButton("->")], [KeyboardButton("<-"), KeyboardButton("->")]]

    @classmethod
    def inline_write(cls, *, titles: list) -> list:
        return [
            [
                InlineKeyboardButton(item[0], **item[1]) if isinstance(item, list) else InlineKeyboardButton(item, callback_data=item)
                for item in row
            ]
            for row in titles
        ]

    @classmethod
    def write(cls, *, titles: list) -> list:
        return [
        [
            KeyboardButton(text[0], **text[1]) if isinstance(text, list) else KeyboardButton(text)
            for text in row
        ]
        for row in titles
    ]

    @classmethod
    def num_construct(cls, *, elements: int, page: int = 0) -> list:
        buttons_per_page = cls.buttons_per_page
        total_pages = max(1, (elements + buttons_per_page - 1) // buttons_per_page)
        page = max(0, min(page, total_pages - 1))

        first_num = page * buttons_per_page + 1
        last_num = min(first_num + buttons_per_page, elements + 1)

        button_numbers = range(first_num, last_num)
        n_buttons = last_num - first_num
        rows = [
            [KeyboardButton(str(num)) for num in button_numbers[i:i+4]]
            for i in range(0, n_buttons, 4)
        ]

        nav_buttons = []
        if page > 0:
            nav_buttons.append(KeyboardButton("<-"))
        if page < total_pages - 1:
            nav_buttons.append(KeyboardButton("->"))
        if nav_buttons:
            rows.append(nav_buttons)

        return rows

    @classmethod
    def dict_construct(cls, *, num_dict: dict[int, str]) -> list[list[KeyboardButton]]:
        return [[KeyboardButton(f"{number}: {value}")] for number, value in sorted(num_dict.items())]

class MenuKeyboard(BaseKeyboard):
    @classmethod
    def main_menu(cls) -> ReplyKeyboardMarkup:
        keyboard = cls.write(titles=[
            ["Добавить контакт 📲"],
            ["Написать список 📝"],
            ["Мои списки", "Полученные списки"],
            ["Контакты"]
        ])
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


class ContactKeyboard(BaseKeyboard):
    @classmethod
    def contacts(cls, *, contacts: dict[int: str], nav: int = None) -> ReplyKeyboardMarkup:
        keyboard = cls.construct(contacts=contacts)
        keyboard.append([KeyboardButton("Добавить контакт", request_contact=True)])
        if nav:
            keyboard.append(cls.nav_variants[nav])
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    @classmethod
    def add_contact(cls) -> ReplyKeyboardMarkup:
        keyboard = cls.write(titles=[
            [["Обрати контакт 👆", {"request_contact": True}]]
        ])
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

class TechnicalKeyboard(BaseKeyboard):
    @classmethod
    def choise_lang(cls) -> InlineKeyboardMarkup:
        keyboard = cls.inline_write(titles=[
            [ [_(key='lang', lang='en'), {"callback_data": 'en'}], [_(key='lang', lang='ua'), {"callback_data": 'ua'}] ]
        ])
        return InlineKeyboardMarkup(keyboard)