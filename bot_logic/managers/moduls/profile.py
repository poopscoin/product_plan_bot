from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from mlangm import translate as _

from .objects.plan import Plan
from .objects.products import ProductBuilder, Product
from .objects.keyboard import ReplyKeyboard

class Profile():
    def __init__(self, id: int):
        self._id = id
        self._create_date = datetime.today().date()

        self._received_plans = {}
        self._created_plans = {}
        # [index: [id, name]]
        self._contacts_num = {0: 12345678}
        self._contacts_id = {12345678: 'Test Contact'}

        self._user_meta = {
            'lang': 'en',
            'state': None,
            'before_state': None,
            'last_message': None,
            'notifications': False,
            'current_plan_id': None,
            'building_product': None,
            'one_panel_page': 0
        }
        # [Name: Type, //Cost_per_one]
        self._user_products = {}
        self._notifications = []
        self._last_action = None
        self._last_keyboard = None

    # NEW_PLAN = 'messages.notifs.receive_plan'

    @property
    def page(self) -> int:
        return self._user_meta['one_panel_page']

    @page.setter
    def page(self, vector: int):
        if self._user_meta['one_panel_page'] == 0 and vector == -1:
            return
        if vector not in (1, -1):
            return
        self._user_meta['one_panel_page'] += vector

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

    @property
    def old_keyboard_state(self):
        return self._user_meta['before_state']

    @keyboard_state.setter
    def keyboard_state(self, new_state):
        if new_state != self.keyboard_state:
            self._user_meta['before_state'] = self.keyboard_state
            self._user_meta['one_panel_page'] = 0
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
    def contacts(self) -> dict[int, int]:
        """Returns a dictionary by IDs, 1 dictionary as opposed to an index dictionary."""
        return self._contacts_id

    @property
    def format_contact(self) -> dict[int, str]:
        """Returns the contact format index - Name."""
        return {
            index: self._contacts_id[user_id]
            for index, user_id in self._contacts_num.items()
        }
    

    # Example Note
    # self._contacts_num = {0: 12345678}
    # self._contacts_id = {12345678: 'Test Contact'}
    def add_contact(self, user_id: int, user_name: str):
        self._contacts_num[len(self._contacts_num)] = user_id
        self._contacts_id[user_id] = user_name

    def get_contact(self, index: int) -> int|None:
        """Search for a contact by position in the list, method 2, with index dictionary"""
        return self._contacts_num.get(index)

    def change_lang(self):
        change_lang = {'en': 'ua', 'ua': 'en'}
        self._user_meta['lang'] = change_lang[self._user_meta['lang']]
        return self._user_meta['lang']

    def notif_viewed(self):
        self._user_meta['notifications'] = False

    def reset_page(self):
        self._user_meta['one_panel_page'] = 0

    # Gets Plans
    def get_receive_plan(self, plan: Plan):
        index = len(self._received_plans)
        self._received_plans[index] = plan
        self.notif = {'data': plan}

    def building_plan(self, value: str|int|float):
        if self.building_product is None:
            self.building_product = ProductBuilder()
        return self.building_product.build(value)

    # def remove_receive_plan(self, *, index: int = 0):
    #     del self._received_plans[index]

    # def clear_receive_plans(self):
    #     self._received_plans = {}

    # Self Plans
    def new_plan(self, *, product_list: dict[int, Product] = None, title: str = None) -> Plan:
        index = len(self._created_plans)
        self.last_plan_id = index
        self._created_plans[index] = Plan(index, product_list=product_list, title=title, lang=self.language)
        return self._created_plans[index]

    def invest_plan(self, plan, *, index: int = None):
        ...

    def get_plan(self, index: int = 1) -> Plan | None:
        return self._created_plans.get(index)

    def remove_my_plan(self, index: int):
        del self._created_plans[index]

    def new_plan_crash(self, full_crash: bool = True):
        self.remove_my_plan(self.last_plan_id)
        self.last_plan_id = None
        self.building_product = None

    async def send_plan(self, update: Update, context: ContextTypes.DEFAULT_TYPE, index: int = None) -> bool:
        plan = self.get_plan(self.last_plan_id)
        if not plan: return None
        try: 
            contact = await context.bot.get_chat(index)
        except:
            return False
        