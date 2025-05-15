from .plan import Plan
from ..moduls.profile import Profile

class User:
    def __init__(self, *, user_id: int):
        self._id = user_id
        self._current_keyboard_id = None
        self._profile = self._get_profile(user_id=user_id)

    @property
    def id(self):
        return self._id
    
    def _get_profile(self, *, user_id: int) -> Profile:
        return Profile()
    