from telegram import KeyboardButton, KeyboardButtonRequestUsers, InlineKeyboardButton
from mlangm import translate as _

from .products import ProductBuilder

class BaseMarkup:
    _BUTTONS_PER_PAGE = 8
    _NAV_VARIANTS = [[KeyboardButton("<-")], [KeyboardButton("->")], [KeyboardButton("<-"), KeyboardButton("->")]]

    @classmethod
    def _inline_write(cls, *, titles: list) -> list[list[KeyboardButton]]:
        return [
            [
                InlineKeyboardButton(item[0], **item[1]) if isinstance(item, list) else InlineKeyboardButton(item, callback_data=item)
                for item in row
            ]
            for row in titles
        ]

    @classmethod
    def _write(cls, *, titles: list) -> list[list[KeyboardButton]]:
        return [
        [
            KeyboardButton(text=text[0], **text[1]) if isinstance(text, list) else KeyboardButton(text)
            for text in row
        ]
        for row in titles
    ]
    
    @classmethod
    def _add_reque_user(cls, *, text: str):
        return [[KeyboardButton(text=text, request_users=KeyboardButtonRequestUsers(request_id=1, user_is_bot=False, max_quantity=1))]]

    @classmethod
    def _num_construct(cls, *, elements: int, page: int = 0) -> list[list[KeyboardButton]]:
        total_pages = max(1, (elements + cls._BUTTONS_PER_PAGE - 1) // cls._BUTTONS_PER_PAGE)
        page = max(0, min(page, total_pages - 1))

        first_num = page * cls._BUTTONS_PER_PAGE + 1
        last_num = min(first_num + cls._BUTTONS_PER_PAGE, elements + 1)

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
    def _dict_construct(cls, *, num_dict: dict[int, str]) -> list[list[KeyboardButton]]:
        return [[KeyboardButton(f"{number}: {value}")] for number, value in sorted(num_dict.items())]

class MenuMarkup(BaseMarkup):

    @classmethod
    def main_menu(cls, lang: str = 'en') -> list[list[KeyboardButton]]:
        if lang == 'ua': change_lang = 'en'
        else: change_lang = 'ua'
        return cls._write(titles=[
            [_('buttons.menu.new_list', lang)],
            [_('buttons.menu.my_lists', lang)],
            [_('buttons.menu.received_list', lang)],
            [_('buttons.menu.change_lang', change_lang)]
        ])

    @classmethod
    def notification_button(cls, lang: str = 'en') -> list[list[KeyboardButton]]:
        return cls._write(titles=[ [_('buttons.menu.notification', lang)] ])

class TechnicalMarkup(BaseMarkup):

    @classmethod
    def inline_choise_lang(cls) -> list[list[KeyboardButton]]:
        return cls._inline_write(titles=[
            [ [_(key='lang', lang='en'), {"callback_data": 'change_lang|en'}], [_(key='lang', lang='ua'), {"callback_data": 'change_lang|ua'}] ]
        ])

class WritePlanMarkup(BaseMarkup):

    @classmethod
    def redact_plan(cls, lang: str = 'en'):
        controls = [[_('buttons.new_plan.go_new', lang), _('buttons.system.back', lang)]]
        markup = [[_('buttons.new_plan.send', lang)],[_('buttons.new_plan.new_product', lang), _('buttons.new_plan.save', lang)]]
        return cls._write(titles=markup+controls)

    @classmethod
    def continue_plan(cls, lang: str = 'en'):
        back = [[_('buttons.system.back', lang)]]
        markup = [[_('buttons.new_plan.continue', lang), _('buttons.new_plan.go_new', lang)]]
        return cls._write(titles=markup+back)

    @classmethod
    def get_next_markup(cls, info: str, lang: str = 'en', plan_present: bool = False, *, product_history: dict|None = None):
        match info:
            case ProductBuilder.NAME:
                return cls._name(lang, product_history, plan_present)
            case ProductBuilder.COUNT:
                return cls._count(lang, plan_present)

    @classmethod
    def _name(cls, lang: str = 'en', product_history: dict|None = None, plan_present: bool = False):
        if product_history:
            ...
        else:
            history = [[_('buttons.new_plan.history_placeholder', lang)]]
        controls = [[_('buttons.system.back', lang)]]
        if plan_present:
            controls[0].insert(0, _('buttons.new_plan.go_plan', lang))
        markup = history + controls
        return cls._write(titles=markup)
    
    @classmethod
    def _count(cls, lang: str = 'en', plan_present: bool = False):
        controls = [[_('buttons.system.cancel', lang), _('buttons.system.back', lang)]]
        if plan_present:
            controls[0].insert(0, _('buttons.new_plan.go_plan', lang))
        markup = [
            [f'500{_('gr', lang)}', f'1{_('kg', lang)}', f'1.5{_('kg', lang)}', f'3{_('kg', lang)}'],
            [f'500{_('ml', lang)}', f'1{_('l', lang)}', f'1.5{_('l', lang)}', f'2{_('l', lang)}'],
            [f'1{_('pcs', lang)}', f'2{_('pcs', lang)}', f'3{_('pcs', lang)}', f'5{_('pcs', lang)}']
        ]
        return cls._write(titles=markup+controls)

# class ContactKeyboard(BaseMarkup):

#     @classmethod
#     def contacts(cls, *, contacts: dict[int: str], nav: int = None) -> list[list[KeyboardButton]]:
#         keyboard = cls.construct(contacts=contacts)
#         keyboard.append([KeyboardButton("Добавить контакт", request_contact=True)])
#         if nav:
#             keyboard.append(cls._NAV_VARIANTS[nav])
#         return keyboard

#     @classmethod
#     def add_contact(cls) -> list[list[KeyboardButton]]:
#         return cls._write(titles=[
#             [["Обрати контакт 👆", {"request_contact": True}]]
#         ])
