from datetime import datetime
from ..objects.plan import Plan

class Profile():
    def __init__(self):
        self._create_date = datetime.today()

        self._received_plans = {}
        self._created_plans = {}
        self._contacts = {}

        self._user_meta = {}
        self._last_action = None
        self._last_keyboard = None

        self._admin = False

    @property
    def keyboard(self):
        return self._last_keyboard

    @property
    def my_plans(self):
        return self._created_plans

    @property
    def received_plans(self):
        return self._received_plans

    @property
    def contacts(self):
        return self._contacts

    @keyboard.setter
    def set_keyboard(self, *, current_keyboard: 'BaseKeyboard'):
        self._last_keyboard = current_keyboard

    @my_plans.setter
    def add_my_plan(self, plan: Plan):
        new_id = max(self._created_plans.keys(), default=0) + 1 
        self._created_plans[new_id] = plan
    
    @received_plans.setter
    def add_receive_plan(self, plan: Plan):
        new_id = max(self._received_plans.keys(), default=0) + 1 
        self._received_plans[new_id] = plan

    def remove_receive_plan(self, *, index: int = 1):
        del self._received_plans[index]

    def clear_receive_plans(self):
        self._received_plans = {}

    def write_new_plan(self) -> tuple[Plan, int]:
        new_id = max(self._created_plans.keys(), default=0) + 1
        new_plan = Plan()
        self._created_plans[new_id] = new_plan
        return new_plan, new_id 

    def continue_write_plan(self, *, index: int = 1) -> Plan:
        return self._created_plans[index]

    def remove_my_plan(self, *, index: int):
        del self._created_plans[index]
