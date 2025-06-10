from datetime import datetime
from .objects.plan import Plan

from .objects.products import ProductBuilder, Product
from .objects.keyboard import ReplyKeyboard

class Profile():
    def __init__(self, id: int):
        self._id = id
        self._create_date = datetime.today().date()

        self._received_plans = {}
        self._created_plans = {}
        # [id: Name, //emoji]
        self._contacts = {}

        self._user_meta = {
            'lang': 'en',
            'state': None,
            'last_message': None,
            'notifications': False,
            'current_plan_id': None,
            'building_product': None,
        }
        # [Name: Type, //Cost_per_one]
        self._user_products = {}
        self._notifications = []
        self._last_action = None
        self._last_keyboard = None
    
    @property
    def building_product(self) -> ProductBuilder | None:
        return self._user_meta['building_product']
    
    @building_product.setter
    def building_product(self, product_builder):
        self._user_meta['building_product'] = product_builder

    @property
    def product_history(self) -> dict|None:
        return self._user_products or None

    @property
    def last_plan_id(self):
        return self._user_meta['current_plan_id']
    
    @last_plan_id.setter
    def last_plan_id(self, id: int|None):
        self._user_meta['current_plan_id'] = id

    @property
    def notif(self):
        return self._notifications

    @notif.setter
    def notif(self, new_notif):
        self._notifications.append(new_notif)
        self._user_meta['notifications'] = True

    @property
    def id(self):
        return self._id

    @property
    def language(self):
        return self._user_meta['lang']

    @language.setter
    def language(self, lang: str):
        self._user_meta['lang'] = 'ua' if lang in ['ru', 'uk'] else 'en'

    @property
    def message(self):
        return self._user_meta['last_message']

    @message.setter
    def message(self, new_last_message: int):
        self._user_meta['last_message'] = new_last_message

    @property
    def keyboard_state(self):
        return self._user_meta['state']

    @keyboard_state.setter
    def keyboard_state(self, new_state: str):
        self._user_meta['state'] = new_state

    @property
    def keyboard(self) -> ReplyKeyboard:
        return self._last_keyboard

    @keyboard.setter
    def keyboard(self, current_keyboard: ReplyKeyboard):
        self._last_keyboard = current_keyboard

    @property
    def my_plans(self):
        return self._created_plans

    @property
    def received_plans(self):
        return self._received_plans

    @property
    def contacts(self) -> dict|bool:
        return self._contacts or False
    
    # def func_crash(self):
    #     self._user_meta['current_func'] = None

    def change_lang(self):
        change_lang = {'en': 'ua', 'ua': 'en'}
        self._user_meta['lang'] = change_lang[self._user_meta['lang']]
        return self._user_meta['lang']

    def notif_viewed(self):
        self._user_meta['notifications'] = False

    # Gets Plans
    def building_plan(self, value: str|int|float):
        if self.building_product is None:
            self.building_product = ProductBuilder()
        return self.building_product.build(value)

    def remove_receive_plan(self, *, index: int = 0):
        del self._received_plans[index]

    def clear_receive_plans(self):
        self._received_plans = {}

    # Self Plans
    def new_plan(self, *, product_list: dict[int, Product] = None, title: str = None) -> Plan:
        index = len(self._created_plans)
        self.last_plan_id = index
        self._created_plans[index] = Plan(index, product_list=product_list, title=title, lang=self.language)
        return self._created_plans[index]

    def get_plan(self, index: int = 1) -> Plan:
        return self._created_plans.get(index)

    def remove_my_plan(self, index: int):
        del self._created_plans[index]

    def new_plan_crash(self, full_crash: bool = True):
        self.remove_my_plan(self.last_plan_id)
        self.last_plan_id = None
        self.building_product = None
